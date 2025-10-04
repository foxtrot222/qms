from flask import Blueprint,render_template , redirect ,url_for ,flash, jsonify ,session
from models.db import get_db_connection
import mysql.connector

status_bp=Blueprint('status',__name__)

@status_bp.route('/status')
def status_page():
    if 'verified_token' not in session:
        flash("Please verify your token first.", "error")
        return redirect(url_for('home'))
    return render_template('status.html')

@status_bp.route('/get_status_details')
def get_status_details():
    token_value = session.get('verified_token')
    if not token_value:
        return jsonify({"success": False, "error": "No verified token in session."})

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True, dictionary=True)

    try:
        cursor.execute("""
            SELECT c.name, c.email AS contact, s.name AS service, t.type, t.id as token_id
            FROM customer c
            JOIN token t ON c.token_id = t.id
            JOIN service s ON c.service_id = s.id
            WHERE t.value = %s
        """, (token_value,))
        details = cursor.fetchone()

        if not details:
            return jsonify({"success": False, "error": "Invalid token."})

        if details['type'] == 'walkin':
            cursor.execute("SELECT TIME_FORMAT(ETR, '%H:%i:%S') as ETR, position FROM walkin WHERE token_id = %s", (details['token_id'],))
            walkin_details = cursor.fetchone()
            if walkin_details:
                details.update(walkin_details)
        elif details['type'] == 'appointment':
            cursor.execute("SELECT TIME_FORMAT(time_slot, '%h:%i %p') as time_slot FROM appointment WHERE token_id = %s", (details['token_id'],))
            appointment_details = cursor.fetchone()
            if appointment_details:
                details.update(appointment_details)
            details['status'] = 'Confirmed'

    except Exception as e:
        print(f"Error fetching status details: {e}")
        return jsonify({"success": False, "error": "An error occurred while fetching details."})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True, "details": details})

# Get Services
@status_bp.route("/get_services")
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