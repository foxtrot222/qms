from flask import Blueprint , request , jsonify ,session
import mysql.connector
import logging
from utils.email_utils import send_token_email
from models.db import get_db_connection

token_bp = Blueprint('token', __name__)
logging.basicConfig(level=logging.INFO)


def generate_next_token():
    """Generates the next token based on the last token in the database."""
    conn = get_db_connection()
    if not conn:
        logging.warning("No DB connection — returning default token A00")
        return 'A00'
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT value FROM token ORDER BY id DESC LIMIT 1")
            last_token_record = cursor.fetchone()
        conn.close()

        if not last_token_record:
            return 'A00'

        last_token = last_token_record['value']
        letter, number = last_token[0], int(last_token[1:])
        if number < 99:
            number += 1
        else:
            number = 0
            letter = chr(ord(letter) + 1) if letter != 'Z' else 'A'
        return f"{letter}{number:02d}"

    except mysql.connector.Error as err:
        logging.error(f"Database query for last token failed: {err}")
        return 'A00'

# Generate Token
@token_bp.route("/generate_token", methods=['POST'])
def generate_token_route():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})
    try:
        name = request.form.get('name')
        email = request.form.get('emailAddress')
        service_id = request.form.get('service')

        if not name or not email or not service_id:
            return jsonify({"success": False, "error": "Missing required fields."})

        cursor = conn.cursor()
        # Create Customer
        cursor.execute("INSERT INTO customer (name, email, service_id) VALUES (%s, %s, %s)", (name, email, service_id))
        customer_id = cursor.lastrowid

        # Generate Token
        new_token_value = generate_next_token()
        cursor.execute("INSERT INTO token (value, customer_id, type) VALUES (%s, %s, %s)", (new_token_value, customer_id, service_id))
        token_id = cursor.lastrowid
        cursor.execute("UPDATE customer SET token_id=%s WHERE id=%s", (token_id, customer_id))

        conn.commit()
        cursor.close()
        conn.close()

        try:
            send_token_email(email, new_token_value)
        except Exception as e:
            print("Failed to send email:", e)

        return jsonify({"success": True, "token": new_token_value})
    except mysql.connector.Error as err:
        print("Database query failed:", err)
        conn.rollback()
        return jsonify({"success": False, "error": "Database error occurred."})

@token_bp.route('/cancel_token', methods=['POST'])
def cancel_token():
    token_value = session.get('verified_token')
    if not token_value:
        return jsonify({"success": False, "error": "No verified token in session."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, type FROM token WHERE value = %s", (token_value,))
        token_record = cursor.fetchone()
        if not token_record:
            session.clear()
            return jsonify({"success": True, "message": "Token already cancelled."})
        
        token_id = token_record['id']
        service_id_str = token_record['type']

        # If it's a walk-in, delete from the corresponding service table
        if service_id_str and service_id_str != 'appointment':
            try:
                service_id = int(service_id_str)
                cursor.execute("SELECT name FROM service WHERE id = %s", (service_id,))
                service_record = cursor.fetchone()
                if service_record:
                    table_name = service_record['name'].lower()
                    cursor.execute(f"DELETE FROM {table_name} WHERE token_id = %s", (token_id,))
            except (ValueError, TypeError):
                pass  # Type is not a valid service ID

        # Handle appointment cancellation
        cursor.execute("UPDATE appointment SET is_booked = 0, token_id = NULL WHERE token_id = %s", (token_id,))
        
        # Delete the token, which should cascade to customer
        cursor.execute("DELETE FROM token WHERE id = %s", (token_id,))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error cancelling token: {e}")
        return jsonify({"success": False, "error": "An error occurred while cancelling the token."})
    finally:
        cursor.close()
        conn.close()

    session.clear()
    return jsonify({"success": True, "message": "Token cancelled successfully."})