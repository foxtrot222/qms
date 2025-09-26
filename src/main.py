from flask import Flask, request, render_template, redirect, url_for, session, flash , jsonify
from dotenv import load_dotenv
import os
import mysql.connector

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

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
def home():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    conn=get_db_connection()
    officerId = request.form.get('officerId')
    officerPassword = request.form.get('officerPassword')

    if not officerId or not officerPassword:
        return jsonify({"success": False, "error": "Provide both ID and password."})

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM service_provider WHERE officerID=%s AND password=%s"
        cursor.execute(query, (officerId, officerPassword))
        officer = cursor.fetchone()
        cursor.close()

        if officer:
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

if __name__ == "__main__":
    app.run(debug=True)
