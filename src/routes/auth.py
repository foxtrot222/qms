from models.db import get_db_connection
import mysql.connector
from flask import Blueprint,render_template , request , redirect ,url_for ,flash, jsonify ,session
from werkzeug.security import check_password_hash
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/")
def home():
    return render_template("index.html")

# Officer Login
@auth_bp.route('/login', methods=['POST'])
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

@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must login first.", "error")
        return redirect(url_for("auth.home"))
    officer_name = session.get('username')
    officer_id = session.get('officer_id_string')
    return render_template("dashboard.html", officer_name=officer_name, officer_id=officer_id)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.home"))