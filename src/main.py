from flask import Flask, request, render_template, redirect, url_for, session, flash , jsonify
from dotenv import load_dotenv
import os
import mysql.connector
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
            session['officer_id'] = officer['officerID']
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
    if "officer_id" not in session:
        flash("You must login first.", "error")
        return redirect(url_for("home"))

    officer_name = session.get('username')
    officer_id = session.get('officer_id')
    return render_template("dashboard.html", officer_name=officer_name, officer_id=officer_id)


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

        return jsonify({"success": True, "token": new_token_value})

    except mysql.connector.Error as err:
        print("Database query failed:", err)
        conn.rollback()
        return jsonify({"success": False, "error": "Database error occurred."})


import logging

# ... (rest of the imports)

# Configure logging
logging.basicConfig(level=logging.INFO)

# ... (rest of the code)

import datetime

# ... (rest of the imports)

# ... (rest of the code)

@app.route("/get_appointment_slots")
def get_appointment_slots():
    logging.info("Attempting to fetch appointment slots.")
    try:
        conn = get_db_connection()
        if not conn:
            logging.error("Database connection failed.")
            return jsonify({"success": False, "error": "Database connection failed."})
        
        logging.info("Database connection successful. Executing query.")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, time_slot FROM appointment WHERE is_booked = 0 ORDER BY time_slot")
        slots = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info(f"Found {len(slots)} available slots.")

        # Convert time objects to strings
        for slot in slots:
            if 'time_slot' in slot and isinstance(slot['time_slot'], datetime.timedelta):
                total_seconds = slot['time_slot'].total_seconds()
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_obj = datetime.time(int(hours), int(minutes), int(seconds))
                slot['time_slot'] = time_obj.strftime('%I:%M %p')

        return jsonify({"success": True, "slots": slots})

    except mysql.connector.Error as err:
        logging.error(f"Database query failed: {err}")
        return jsonify({"success": False, "error": "Database error occurred."})
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"success": False, "error": "An unexpected error occurred."})


if __name__ == "__main__":
    # Run the app on the port from .env or default to 5000
    app.run(debug=True, port=port)
