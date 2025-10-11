from models.db import get_db_connection
import mysql.connector
from flask import Blueprint,render_template , request , redirect ,url_for ,flash, jsonify ,session
from werkzeug.security import check_password_hash
org_bp = Blueprint('org', __name__)

@org_bp.route('/')
def organization():
    return render_template('organization.html')

@org_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('org.organization'))

    officer_name = session.get('username')
    officer_id = session.get('officer_id_string')
    return render_template('dashboard.html', officer_name=officer_name, officer_id=officer_id)

@org_bp.route('/login', methods=['GET','POST'])
def login():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed. Please try again later.")
        return redirect(url_for("org.login"))
    officerId = request.form.get('officerId')
    officerPassword = request.form.get('officerPassword')

    if not officerId or not officerPassword:
        return jsonify({"success": False, "error": "Provide both ID and password."})

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM service_provider WHERE officerID=%s", (officerId,))
        officer = cursor.fetchone()

        if officer and check_password_hash(officer['password'], officerPassword):
            # Get service details
            cursor.execute("SELECT name FROM service WHERE id = %s", (officer['service_id'],))
            service_record = cursor.fetchone()
            table_name = service_record['name'].lower() if service_record else None
            
            cursor.close()

            session['user_id'] = officer['id']
            session['username'] = officer['name']
            session['officer_id_string'] = officer['officerID']
            session['service_id'] = officer['service_id']
            session['table_name'] = table_name

            return jsonify({"success": True, "redirect": "/dashboard", "officerName": officer['name']})
        else:
            cursor.close()
            return jsonify({"success": False, "error": "Invalid ID or password."})
    except mysql.connector.Error as err:
        print("Database query failed:", err)
        return jsonify({"success": False, "error": "Database error occurred."})

@org_bp.route("/org/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("org.organization"))