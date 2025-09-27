from flask import Flask, request, render_template, redirect, url_for, session, flash , jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

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



if __name__ == "__main__":
    # Run the app on the port from .env or default to 5000
    app.run(debug=True, port=port)
