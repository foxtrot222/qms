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
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id AS customer_id, c.email
        FROM customer c
        JOIN token t ON c.token_id = t.id
        WHERE t.value = ?
    """, (token,))
    customer = cursor.fetchone()

    if not customer:
        return jsonify({"success": False, "error": "Invalid token."})

    # Check for existing OTP not expired
    cursor.execute("""
        SELECT * FROM otp_verification
        WHERE customer_id = ? AND verified=FALSE AND expires_at > datetime('now')
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
            "INSERT INTO otp_verification (customer_id, otp_code, expires_at) VALUES (?, ?, ?)",
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
    cursor = conn.cursor()

    cursor.execute("""
        SELECT otp.id, otp.customer_id, otp.expires_at, otp.verified, t.type, t.id as token_id
        FROM otp_verification otp
        JOIN customer c ON otp.customer_id = c.id
        JOIN token t ON c.token_id = t.id
        WHERE t.value = ? AND otp.otp_code = ?
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
    cursor.execute("DELETE FROM otp_verification WHERE id = ?", (record['id'],))
    conn.commit()

    #Save token in session
    session['verified_token'] = token_value

    token_id = record['token_id']

    query_check = """
        (SELECT token_id FROM billing WHERE token_id = ?)
        UNION ALL
        (SELECT token_id FROM complaint WHERE token_id = ?)
        UNION ALL
        (SELECT token_id FROM kyc WHERE token_id = ?)
        UNION ALL
        (SELECT token_id FROM appointment WHERE token_id = ? AND is_booked = 1)
    """
    cursor.execute(query_check, (token_id, token_id, token_id, token_id))
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
            cursor.execute("DELETE FROM otp_verification WHERE expires_at < datetime('now')")
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print("Failed to cleanup expired OTPs:", e)
