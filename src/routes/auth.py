from flask import Blueprint, jsonify, request
import sqlite3
import time
from models.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/estimated_wait_time')
def estimated_wait_time():
    service_id = request.args.get('service_id')
    if not service_id:
        return jsonify({"success": False, "error": "Service ID is required."})

    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})

    try:
        cursor = conn.cursor()

        # Get table name from service_id
        cursor.execute("SELECT name FROM service WHERE id = ?", (service_id,))
        service = cursor.fetchone()
        if not service:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "error": "Invalid service ID."})
        table_name = service['name'].lower()

        # Get average service time from logs
        cursor.execute("SELECT AVG((strftime('%s', log) - strftime('%s', '00:00:00'))) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time = float(avg_time_result['avg_time']) if avg_time_result and avg_time_result['avg_time'] else 180.0

        # Get current queue length
        cursor.execute(f"SELECT COUNT(*) as queue_length FROM {table_name}")
        queue_length = cursor.fetchone()['queue_length']

        # Calculate estimated wait time
        total_wait_seconds = queue_length * avg_service_time
        estimated_time = time.strftime('%H:%M:%S', time.gmtime(total_wait_seconds))

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "estimated_wait_time": estimated_time
        })

    except sqlite3.Error as e:
        # Log the error for debugging
        print(f"Database error in estimated_wait_time: {e}")
        return jsonify({"success": False, "error": f"Database error: {str(e)}"})

    except Exception as e:
        # Log the error for debugging
        print(f"Unexpected error in estimated_wait_time: {e}")
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"})
