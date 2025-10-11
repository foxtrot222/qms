from models.db import get_db_connection
import mysql.connector
from flask import Blueprint, jsonify, request
import time

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/estimated_wait_time')
def estimated_wait_time():
    service_id = request.args.get('service_id', type=int)
    if not service_id:
        return jsonify({"success": False, "error": "Service ID is required."})

    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})

    try:
        cursor = conn.cursor(dictionary=True)

        # Get table name from service id
        cursor.execute("SELECT name FROM service WHERE id = %s", (service_id,))
        service_record = cursor.fetchone()
        if not service_record:
            return jsonify({"success": False, "error": "Invalid service."})
        
        table_name = service_record['name'].lower()

        # Calculate average service time from logs
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time = float(avg_time_result['avg_time'] or 180) # default to 180s (3 min)

        # Get number of people in the queue
        cursor.execute(f"SELECT COUNT(*) as queue_length FROM {table_name}")
        queue_length_result = cursor.fetchone()
        queue_length = queue_length_result['queue_length']

        # Estimated wait time = (people in queue) * avg_service_time
        etr_in_seconds = queue_length * avg_service_time
        etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "estimated_wait_time": etr_formatted
        })

    except mysql.connector.Error as e:
        return jsonify({"success": False, "error": f"Database error: {str(e)}"})
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"})