from models.db import get_db_connection
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import check_password_hash
import logging

# Blueprint setup
org_bp = Blueprint('org', __name__)

# Filter out static logs
class NoStaticFilter(logging.Filter):
    def filter(self, record):
        return '/static/' not in record.getMessage()

log = logging.getLogger('werkzeug')
log.addFilter(NoStaticFilter())


# ------------------------------
# Home (Organization Landing Page)
# ------------------------------
@org_bp.route('/')
def organization():
    return render_template('organization.html')


# ------------------------------
# Officer Dashboard
# ------------------------------
@org_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('org.organization'))

    officer_name = session.get('username')
    officer_id = session.get('officer_id_string')
    return render_template('dashboard.html', officer_name=officer_name, officer_id=officer_id)


# ------------------------------
# Officer Login
# ------------------------------
@org_bp.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed. Please try again later."})

    officer_id = request.form.get('officerId')
    officer_password = request.form.get('officerPassword')

    if not officer_id or not officer_password:
        return jsonify({"success": False, "error": "Provide both ID and password."})

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service_provider WHERE officerID=%s", (officer_id,))
        officer = cursor.fetchone()

        if officer and check_password_hash(officer['password'], officer_password):
            # Fetch related service name
            cursor.execute("SELECT name FROM service WHERE id = %s", (officer['service_id'],))
            service_record = cursor.fetchone()
            table_name = service_record['name'].lower() if service_record else None

            # Store session
            session['user_id'] = officer['id']
            session['username'] = officer['name']
            session['officer_id_string'] = officer['officerID']
            session['service_id'] = officer['service_id']
            session['table_name'] = table_name

            cursor.close()
            return jsonify({"success": True, "redirect": "/dashboard", "officerName": officer['name']})
        else:
            cursor.close()
            return jsonify({"success": False, "error": "Invalid ID or password."})
    except sqlite3.Error as err:
        print("Database query failed:", err)
        return jsonify({"success": False, "error": "Database error occurred."})


# ------------------------------
# Admin Login
# ------------------------------
@org_bp.route('/adminlogin', methods=['POST'])
def admin_login():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed. Please try again later."})

    admin_id = request.form.get('adminID')
    admin_password = request.form.get('adminPassword')

    if not admin_id or not admin_password:
        return jsonify({"success": False, "error": "Provide both ID and password."})

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE adminID=%s", (admin_id,))
        admin = cursor.fetchone()

        if admin and check_password_hash(admin['password'], admin_password):
            # Store session
            session['admin_id'] = admin['id']
            session['admin_name'] = admin['name']

            cursor.close()
            return jsonify({"success": True, "redirect": "/admin/dashboard", "adminName": admin['name']})
        else:
            cursor.close()
            return jsonify({"success": False, "error": "Invalid ID or password."})
    except sqlite3.Error as err:
        print("Database query failed:", err)
        return jsonify({"success": False, "error": "Database error occurred."})


# ------------------------------
# Logout (for both officer & admin)
# ------------------------------
@org_bp.route('/org/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('org.organization'))
