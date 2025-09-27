from flask import Flask, request, render_template, redirect, url_for, session, flash , jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from email_utils import send_token_email
import random
from datetime import datetime, timedelta

def generate_otp(length=6):
    """Generates a numeric OTP of given length."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(to_email: str, otp: str):
    """Sends the OTP email using your existing send_token_email function."""
    from email_utils import send_token_email
    send_token_email(otp, to_email)  # Reuse your existing email function


def generate_next_token():
    """Generates the next token based on the last one in the database."""
    conn = get_db_connection()
    if not conn:
        # Handle connection error, maybe return a default or raise an exception
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
                letter = 'A'  # Or handle overflow

        return f"{letter}{number:02d}"

    except mysql.connector.Error as err:
        print("Database query for last token failed:", err)
        # Handle error, maybe return a default or raise an exception
        return 'A00'

# Load the .env file
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "App")

app = Flask(__name__)

# Access values from .env
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")
port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set in the .env

# Define the database connection function
def get_db_connection():
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

@app.route("/")
# Home Page
def home():
    return render_template("index.html")
    
@app.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()  # Use the new function for database connection
    officerId = request.form.get('officerId')
    officerPassword = request.form.get('officerPassword')

    if not officerId or not officerPassword:
        return jsonify({"success": False, "error": "Provide both ID and password."})

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM service_provider WHERE officerID=%s"
        cursor.execute(query, (officerId,))
        officer = cursor.fetchone()
        cursor.close()

        if officer and check_password_hash(officer['password'], officerPassword):
            # Set session for dashboard access
            session['user_id'] = officer['id']
            session['username'] = officer['name']

            # Send JSON for JS redirect
            return jsonify({
                "success": True,
                "redirect": "/dashboard",
                "officerName": officer['name']
            })

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

@app.route("/status")
def status():
    return render_template("status.html")

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

        # Step 1: Create a new customer record
        insert_customer_query = "INSERT INTO customer (name, email, service_id) VALUES (%s, %s, %s)"
        cursor.execute(insert_customer_query, (name, email, service_id))
        customer_id = cursor.lastrowid

        # Step 2: Generate a new token value
        new_token_value = generate_next_token()

        # Step 3: Create a new token record
        insert_token_query = "INSERT INTO token (value, customer_id) VALUES (%s, %s)"
        cursor.execute(insert_token_query, (new_token_value, customer_id))
        token_id = cursor.lastrowid

        # Step 4: Update the customer with the token_id
        update_customer_query = "UPDATE customer SET token_id = %s WHERE id = %s"
        cursor.execute(update_customer_query, (token_id, customer_id))

        conn.commit()
        cursor.close()
        conn.close()

        # Send email here
        try:
            send_token_email(email,new_token_value)
        except Exception as e:
            print("Failed to send email:", e)

        return jsonify({"success": True, "token": new_token_value})

    except mysql.connector.Error as err:
        print("Database query failed:", err)
        conn.rollback()
        return jsonify({"success": False, "error": "Database error occurred."})

@app.route("/request_otp", methods=['POST'])
def request_otp():
    email = request.form.get('email')
    token = request.form.get('token')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verify email + token
    cursor.execute("""
        SELECT c.id AS customer_id
        FROM customer c
        JOIN token t ON c.token_id = t.id
        WHERE c.email=%s AND t.value=%s
    """, (email, token))
    customer = cursor.fetchone()

    if not customer:
        return jsonify({"success": False, "error": "Invalid email or token."})

    # Generate OTP and expiry
    otp_code = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=5)

    # Save OTP to DB
    cursor.execute("""
        INSERT INTO otp_verification (customer_id, otp_code, expires_at)
        VALUES (%s, %s, %s)
    """, (customer['customer_id'], otp_code, expires_at))
    conn.commit()
    cursor.close()
    conn.close()

    # Send OTP email
    try:
        send_otp_email(email, otp_code)
    except Exception as e:
        print("Failed to send OTP email:", e)

    return jsonify({"success": True, "message": "OTP sent to your email."})

@app.route("/verify_otp", methods=['POST'])
def verify_otp():
    email = request.form.get('email')
    otp = request.form.get('otp')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT otp.id, otp.customer_id, otp.expires_at, otp.verified
        FROM otp_verification otp
        JOIN customer c ON otp.customer_id = c.id
        WHERE c.email=%s AND otp_code=%s
        ORDER BY otp.id DESC LIMIT 1
    """, (email, otp))

    record = cursor.fetchone()
    if not record:
        return jsonify({"success": False, "error": "Invalid OTP."})

    if record['verified']:
        return jsonify({"success": False, "error": "OTP already used."})

    if record['expires_at'] < datetime.now():
        return jsonify({"success": False, "error": "OTP expired."})

    # Mark OTP as verified
    cursor.execute("UPDATE otp_verification SET verified=TRUE WHERE id=%s", (record['id'],))
    conn.commit()
    cursor.close()
    conn.close()

    # Successful login, set session
    session['user_id'] = record['customer_id']
    return jsonify({"success": True, "message": "OTP verified, logged in."})



if __name__ == "__main__":
    # Run the app on the port from .env or default to 5000
    app.run(debug=True, port=port)
