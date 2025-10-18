from flask import Blueprint, request , jsonify ,session
from models.db import get_db_connection
from utils.email_utils import send_otp_email
from datetime import datetime, timedelta
import random

def generate_otp(length=6):
    """Generates a numeric OTP of given length."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

otp_bp=Blueprint('otp',__name__)

# Request OTP
@otp_bp.route("/request_otp", methods=['POST'])
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
@otp_bp.route("/verify_otp", methods=['POST'])
def verify_otp():
    data = request.get_json()
    token_value = data.get('token')
    otp = data.get('otp')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT otp.id, otp.customer_id, otp.expires_at, otp.verified, t.type, t.id as token_id
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

    #Save token in session
    session['verified_token'] = token_value

    token_id = record['token_id']

    cursor.execute("SELECT name FROM service")
    services = cursor.fetchall()
    
    query_parts = []
    params = []
    for service in services:
        table_name = service['name']
        query_parts.append(f"(SELECT token_id FROM {table_name} WHERE token_id = %s)")
        params.append(token_id)

    query_parts.append("(SELECT token_id FROM appointment WHERE token_id = %s AND is_booked = 1)")
    params.append(token_id)

    query_check = " UNION ALL ".join(query_parts)
    
    cursor.execute(query_check, tuple(params))
    existing_queue_or_appointment = cursor.fetchone()

    cursor.close()
    conn.close()

    if existing_queue_or_appointment:
        return jsonify({"success": True, "action": "redirect_status", "message": "OTP verified, access granted."})
    else:
        return jsonify({"success": True, "action": "choose_type", "service_id": record['type']})
    
@otp_bp.before_request
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
