from flask import Blueprint, request, jsonify, session
import sqlite3
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
        with conn.cursor() as cursor:
            cursor.execute("SELECT value FROM token ORDER BY id DESC LIMIT 1")
            last_token_record = cursor.fetchone()
        conn.close()

        if not last_token_record:
            return 'A00'

        last_token = last_token_record['value']
        letter = last_token[0]

        # Extract only digits after the first character
        number_part = ""
        for ch in last_token[1:]:
            if ch.isdigit():
                number_part += ch
            else:
                break

        number = int(number_part)
        if number < 99:
            number += 1
        else:
            number = 0
            letter = chr(ord(letter) + 1) if letter != 'Z' else 'A'
        return f"{letter}{number:02d}"

    except sqlite3.Error as err:
        logging.error(f"Database query for last token failed: {err}")
        return 'A00'


# ------------------------------------------------------------------
# 🎟️ Generate Token Route
# ------------------------------------------------------------------
@token_bp.route("/generate_token", methods=["POST"])
def generate_token_route():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})

    try:
        name = request.form.get("name")
        consumer_id = request.form.get("consumerId")
        email = request.form.get("emailAddress")
        service_id = request.form.get("service")

        if not name or not service_id:
            return jsonify({"success": False, "error": "Missing required fields (name/service_id)."})
        
        cursor = conn.cursor()

        # Step 1: Resolve email using consumer ID if provided
        if (not email) and consumer_id:
            cursor.execute("SELECT email FROM consumer WHERE consumer_id = ?", (consumer_id,))
            result = cursor.fetchone()
            if result and result.get("email"):
                email = result["email"]
            else:
                return jsonify({"success": False, "error": "Invalid Consumer ID or email not linked."})

        # Step 2: Ensure at least one identifier exists
        if (not email) and (not consumer_id):
            return jsonify({"success": False, "error": "Either email or consumer ID is required."})

        # Step 3: Insert into customer table
        cursor.execute("""
            INSERT INTO customer (name, consumer_id, email, service_id)
            VALUES (?, ?, ?, ?)
        """, (name, consumer_id, email, service_id))
        customer_id = cursor.lastrowid

        # Step 4: Generate next token
        cursor.execute('SELECT s.name as service_name FROM service s JOIN customer c ON s.id=c.service_id WHERE s.id = ? LIMIT 1;',(service_id,))
        service_name=cursor.fetchone()
        new_token_value = generate_next_token()+'-'+service_name['service_name']
        cursor.execute("""
            INSERT INTO token (value, customer_id, type)
            VALUES (?, ?, ?)
        """, (new_token_value, customer_id,service_id))
        token_id = cursor.lastrowid

        # Step 5: Update customer with token ID
        cursor.execute("UPDATE customer SET token_id = %s WHERE id = ?", (token_id, customer_id))
        conn.commit()

        # Step 6: Send token email (if email available)
        if email:
            try:
                send_token_email(email, new_token_value)
            except Exception as e:
                logging.error(f"Failed to send token email: {e}")

        return jsonify({"success": True, "token": new_token_value})

    except sqlite3.Error as err:
        conn.rollback()
        logging.error(f"Database query failed: {err}")
        return jsonify({"success": False, "error": "Database error occurred."})

    finally:
        if conn:
            cursor.close()
            conn.close()


# ------------------------------------------------------------------
# ❌ Cancel Token Route
# ------------------------------------------------------------------
@token_bp.route("/cancel_token", methods=["POST"])
def cancel_token():
    token_value = session.get("verified_token")
    if not token_value:
        return jsonify({"success": False, "error": "No verified token in session."})

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, type FROM token WHERE value = ?", (token_value,))
        token_record = cursor.fetchone()

        if not token_record:
            session.clear()
            return jsonify({"success": True, "message": "Token already cancelled."})
        
        token_id = token_record["id"]
        service_id_str = token_record["type"]

        # 🧾 Delete from service queue if walk-in
        if service_id_str and service_id_str != "appointment":
            try:
                service_id = int(service_id_str)
                cursor.execute("SELECT name FROM service WHERE id = ?", (service_id,))
                service_record = cursor.fetchone()
                if service_record:
                    table_name = service_record["name"].lower()
                    cursor.execute(f"DELETE FROM {table_name} WHERE token_id = ?", (token_id,))
            except (ValueError, TypeError):
                pass  # Not a numeric service id

        # 🗓️ Unbook appointment if needed
        cursor.execute("UPDATE appointment SET is_booked = 0, token_id = NULL WHERE token_id = ?", (token_id,))
        
        # 🧹 Delete the token (cascade removes customer)
        cursor.execute("DELETE FROM token WHERE id = ?", (token_id,))
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        logging.error(f"Error cancelling token: {e}")
        return jsonify({"success": False, "error": "An error occurred while cancelling the token."})

    finally:
        cursor.close()
        conn.close()

    session.clear()
    return jsonify({"success": True, "message": "Token cancelled successfully."})
