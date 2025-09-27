from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from email_utils import send_token_email
import random
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "App")

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

def send_otp_email(to_email: str, otp: str):
    """Sends the OTP email using existing email function."""
    send_token_email(otp, to_email)

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
    return render_template("dashboard.html", officer_name=officer_name)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

# Status Page
@app.route('/status', methods=['GET'])
def status():
    """
    Fetches and displays customer details based on the token stored in session.
    Removes the need to pass token in query string (?token=...).
    """
    # Prefer session token if available
    token = session.get('verified_token')  # get token from session instead of query params

    if not token:
        return jsonify({"success": False, "error": "Token is required."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch customer details
    cursor.execute("""
        SELECT c.name, c.email AS contact, s.name AS service
        FROM customer c
        JOIN token t ON c.token_id = t.id
        JOIN service s ON c.service_id = s.id
        WHERE t.value=%s
    """, (token,))
    
    customer = cursor.fetchone()
    cursor.close()
    conn.close()

    if not customer:
        return jsonify({"success": False, "error": "Invalid token."})

    return jsonify({"success": True, "customer": customer})

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
    token = data.get('token')
    otp = data.get('otp')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT otp.id, otp.customer_id, otp.expires_at, otp.verified
        FROM otp_verification otp
        JOIN customer c ON otp.customer_id = c.id
        JOIN token t ON c.token_id = t.id
        WHERE t.value=%s AND otp_code=%s
        ORDER BY otp.id DESC LIMIT 1
    """, (token, otp))

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
    cursor.close()
    conn.close()

    # ✅ Save token in session
    session['verified_token'] = token

    return jsonify({"success": True, "message": "OTP verified, access granted."})

# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(debug=True, port=port)
