from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from email_utils import send_token_email, send_otp_email
import random
from datetime import datetime, timedelta
import logging
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")
port = int(os.getenv("PORT", 5000))

# ------------------- Helper Functions -------------------

def get_db_connection():
    """Establishes a database connection."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None

def generate_otp(length=6):
    """Generates a numeric OTP of given length."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])



def generate_next_token():
    """Generates the next token based on the last token in the database."""
    conn = get_db_connection()
    if not conn:
        return 'A00'
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT value FROM token ORDER BY id DESC LIMIT 1")
        last_token_record = cursor.fetchone()
        cursor.close()
        conn.close()
        if not last_token_record:
            return 'A00'
        last_token = last_token_record['value']
        letter = last_token[0]
        number = int(last_token[1:])
        if number < 99:
            number += 1
        else:
            number = 0
            letter = chr(ord(letter) + 1)
            if letter > 'Z':
                letter = 'A'
        return f"{letter}{number:02d}"
    except mysql.connector.Error as err:
        print("Database query for last token failed:", err)
        return 'A00'

# ------------------- Cleanup Expired OTPs -------------------

@app.before_request
def cleanup_expired_otps():
    """Automatically deletes expired OTPs before each request."""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM otp_verification WHERE expires_at < NOW()")
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print("Failed to cleanup expired OTPs:", e)

# ------------------- Routes -------------------

@app.route("/")
def home():
    return render_template("index.html")

# Officer Login
@app.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
    officerId = request.form.get('officerId')
    officerPassword = request.form.get('officerPassword')

    if not officerId or not officerPassword:
        return jsonify({"success": False, "error": "Provide both ID and password."})

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM service_provider WHERE officerID=%s", (officerId,))
        officer = cursor.fetchone()
        cursor.close()

        if officer and check_password_hash(officer['password'], officerPassword):
            session['user_id'] = officer['id']
            session['username'] = officer['name']
            session['officer_id_string'] = officer['officerID']
            return jsonify({"success": True, "redirect": "/dashboard", "officerName": officer['name']})
        else:
            return jsonify({"success": False, "error": "Invalid ID or password."})
    except mysql.connector.Error as err:
        print("Database query failed:", err)
        return jsonify({"success": False, "error": "Database error occurred."})

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must login first.", "error")
        return redirect(url_for("home"))
    officer_name = session.get('username')
    officer_id = session.get('officer_id_string')
    return render_template("dashboard.html", officer_name=officer_name, officer_id=officer_id)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

# Status Page
@app.route('/status')
def status_page():
    if 'verified_token' not in session:
        flash("Please verify your token first.", "error")
        return redirect(url_for('home'))
    return render_template('status.html')

@app.route('/get_status_details')
def get_status_details():
    token_value = session.get('verified_token')
    if not token_value:
        return jsonify({"success": False, "error": "No verified token in session."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT c.name, c.email AS contact, s.name AS service, t.type, t.id as token_id
            FROM customer c
            JOIN token t ON c.token_id = t.id
            JOIN service s ON c.service_id = s.id
            WHERE t.value = %s
        """, (token_value,))
        details = cursor.fetchone()

        if not details:
            return jsonify({"success": False, "error": "Invalid token."})

        if details['type'] == 'walkin':
            cursor.execute("SELECT ETR, position FROM walkin WHERE token_id = %s", (details['token_id'],))
            walkin_details = cursor.fetchone()
            if walkin_details:
                details.update(walkin_details)
        elif details['type'] == 'appointment':
            cursor.execute("SELECT TIME_FORMAT(time_slot, '%h:%i %p') as time_slot FROM appointment WHERE token_id = %s", (details['token_id'],))
            appointment_details = cursor.fetchone()
            if appointment_details:
                details.update(appointment_details)
            details['status'] = 'Confirmed'

    except Exception as e:
        print(f"Error fetching status details: {e}")
        return jsonify({"success": False, "error": "An error occurred while fetching details."})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True, "details": details})

# Get Services
@app.route("/get_services")
def get_services():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM service ORDER BY name")
        services = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "services": services})
    except mysql.connector.Error as err:
        print("Database query failed:", err)
        return jsonify({"success": False, "error": "Database error occurred."})

# Generate Token
@app.route("/generate_token", methods=['POST'])
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
        cursor.execute("INSERT INTO token (value, customer_id) VALUES (%s, %s)", (new_token_value, customer_id))
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

# Request OTP
@app.route("/request_otp", methods=['POST'])
def request_otp():
    data = request.get_json()
    token = data.get('token')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id AS customer_id, c.email
        FROM customer c
        JOIN token t ON c.token_id = t.id
        WHERE t.value=%s
    """, (token,))
    customer = cursor.fetchone()

    if not customer:
        return jsonify({"success": False, "error": "Invalid token."})

    # Check for existing OTP not expired
    cursor.execute("""
        SELECT * FROM otp_verification
        WHERE customer_id=%s AND verified=FALSE AND expires_at > NOW()
        ORDER BY id DESC LIMIT 1
    """, (customer['customer_id'],))
    existing_otp = cursor.fetchone()

    if existing_otp:
        otp_code = existing_otp['otp_code']
        expires_at = existing_otp['expires_at']
    else:
        otp_code = generate_otp()
        expires_at = datetime.now() + timedelta(minutes=5)
        cursor.execute(
            "INSERT INTO otp_verification (customer_id, otp_code, expires_at) VALUES (%s, %s, %s)",
            (customer['customer_id'], otp_code, expires_at)
        )
        conn.commit()

    cursor.close()
    conn.close()

    try:
        send_otp_email(customer['email'], otp_code)
    except Exception as e:
        print("Failed to send OTP email:", e)

    return jsonify({"success": True, "message": "OTP sent to your email."})


# Verify OTP
@app.route("/verify_otp", methods=['POST'])
def verify_otp():
    data = request.get_json()
    token_value = data.get('token')
    otp = data.get('otp')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT otp.id, otp.customer_id, otp.expires_at, otp.verified, t.type
        FROM otp_verification otp
        JOIN customer c ON otp.customer_id = c.id
        JOIN token t ON c.token_id = t.id
        WHERE t.value=%s AND otp.otp_code=%s
        ORDER BY otp.id DESC LIMIT 1
    """, (token_value, otp))

    record = cursor.fetchone()

    if not record:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": "Wrong OTP. Please try again."})

    if record['verified']:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": "OTP already used."})

    if record['expires_at'] < datetime.now():
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": "OTP expired."})

    # OTP is correct → delete it
    cursor.execute("DELETE FROM otp_verification WHERE id=%s", (record['id'],))
    conn.commit()

    # ✅ Save token in session
    session['verified_token'] = token_value

    if record['type'] is None:
        cursor.close()
        conn.close()
        return jsonify({"success": True, "action": "choose_type"})
    else:
        cursor.close()
        conn.close()
        return jsonify({"success": True, "action": "redirect_status", "message": "OTP verified, access granted."})

@app.route("/get_queue")
def get_queue():
    logging.info("Attempting to fetch queue data.")
    try:
        conn = get_db_connection()
        if not conn:
            logging.error("Database connection failed.")
            return jsonify({"success": False, "error": "Database connection failed."})
        
        logging.info("Database connection successful. Executing query.")
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
                w.position,
                t.value AS token_value
            FROM
                walkin w
            JOIN
                token t ON w.token_id = t.id
            ORDER BY
                w.position;
        """
        cursor.execute(query)
        queue = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info(f"Found {len(queue)} customers in the queue.")

        return jsonify({"success": True, "queue": queue})

    except mysql.connector.Error as err:
        logging.error(f"Database query failed: {err}")
        return jsonify({"success": False, "error": "Database error occurred."})
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"success": False, "error": "An unexpected error occurred."})


@app.route("/complete_service", methods=['POST'])
def complete_service():
    logging.info("Attempting to complete a service.")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        service_time_seconds = int(request.form.get('service_time', 0))
        if service_time_seconds > 1: # Log only realistic times
            service_time_formatted = time.strftime('%H:%M:%S', time.gmtime(service_time_seconds))
            cursor.execute("INSERT INTO logs (log) VALUES (%s)", (service_time_formatted,))

        # Find the customer being served
        cursor.execute("SELECT token_id FROM walkin WHERE position = 0")
        serving = cursor.fetchone()

        if serving:
            token_id_to_delete = serving['token_id']
            # Remove references from child tables first
            cursor.execute("DELETE FROM walkin WHERE token_id = %s", (token_id_to_delete,))
            cursor.execute("UPDATE appointment SET is_booked = 0, token_id = NULL WHERE token_id = %s", (token_id_to_delete,))
            # Now delete the token, which should cascade to customer
            cursor.execute("DELETE FROM token WHERE id = %s", (token_id_to_delete,))

        # Shift the entire queue up
        cursor.execute("UPDATE walkin SET position = position - 1 WHERE position > 0")

        # Recalculate all ETRs for the remaining queue
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time_decimal = avg_time_result['avg_time'] if avg_time_result['avg_time'] and avg_time_result['avg_time'] > 0 else 180
        avg_service_time = float(avg_service_time_decimal)

        cursor.execute("SELECT id, position FROM walkin ORDER BY position")
        remaining_queue = cursor.fetchall()

        for person in remaining_queue:
            etr_in_seconds = person['position'] * avg_service_time
            etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))
            cursor.execute("UPDATE walkin SET ETR = %s WHERE id = %s", (etr_formatted, person['id']))

        conn.commit()

    except Exception as e:
        conn.rollback()
        logging.error(f"An unexpected error occurred in complete_service: {e}")
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True})


@app.route('/get_available_slots', methods=['GET'])
def get_available_slots():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, TIME_FORMAT(time_slot, '%h:%i %p') as time_slot FROM appointment WHERE is_booked = 0 ORDER BY time_slot")
    slots = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "slots": slots})

@app.route('/join_walkin', methods=['POST'])
def join_walkin():
    data = request.get_json()
    token_value = data.get('token')
    if not token_value:
        return jsonify({"success": False, "error": "Token is required."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM token WHERE value = %s", (token_value,))
        token_record = cursor.fetchone()
        if not token_record:
            return jsonify({"success": False, "error": "Invalid token."})
        token_id = token_record['id']

        # Calculate average service time from logs (defaults to 3 minutes if no logs)
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time = avg_time_result['avg_time'] if avg_time_result['avg_time'] else 180

        # Determine position
        cursor.execute("SELECT id FROM walkin WHERE position = 0")
        serving_now = cursor.fetchone()
        if not serving_now:
            next_pos = 0
        else:
            cursor.execute("SELECT MAX(position) as max_pos FROM walkin")
            max_pos_record = cursor.fetchone()
            next_pos = (max_pos_record['max_pos'] or 0) + 1

        # Calculate ETR (number of people ahead * avg service time)
        etr_in_seconds = next_pos * avg_service_time
        etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))

        # Insert into walkin table
        cursor.execute("INSERT INTO walkin (token_id, position, ETR) VALUES (%s, %s, %s)", (token_id, next_pos, etr_formatted))
        cursor.execute("UPDATE token SET type = 'walkin' WHERE id = %s", (token_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True, "message": "Successfully joined walk-in queue."})

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.get_json()
    token_value = data.get('token')
    slot_id = data.get('slot_id')
    if not token_value or not slot_id:
        return jsonify({"success": False, "error": "Token and slot are required."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM token WHERE value = %s", (token_value,))
        token_record = cursor.fetchone()
        if not token_record:
            return jsonify({"success": False, "error": "Invalid token."})
        token_id = token_record['id']

        cursor.execute("SELECT is_booked FROM appointment WHERE id = %s FOR UPDATE", (slot_id,))
        slot_record = cursor.fetchone()
        if not slot_record:
            return jsonify({"success": False, "error": "Invalid slot."})
        if slot_record['is_booked']:
            conn.rollback()
            return jsonify({"success": False, "error": "Slot already taken."})
        
        cursor.execute("UPDATE appointment SET is_booked = 1, token_id = %s WHERE id = %s", (token_id, slot_id))
        cursor.execute("UPDATE token SET type = 'appointment' WHERE id = %s", (token_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True, "message": "Appointment booked successfully."})

@app.route('/cancel_token', methods=['POST'])
def cancel_token():
    token_value = session.get('verified_token')
    if not token_value:
        return jsonify({"success": False, "error": "No verified token in session."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM token WHERE value = %s", (token_value,))
        token_record = cursor.fetchone()
        if not token_record:
            session.clear()
            return jsonify({"success": True, "message": "Token already cancelled."})
        token_id = token_record['id']

        cursor.execute("DELETE FROM walkin WHERE token_id = %s", (token_id,))
        cursor.execute("UPDATE appointment SET is_booked = 0, token_id = NULL WHERE token_id = %s", (token_id,))
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


# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(debug=True, port=port)
