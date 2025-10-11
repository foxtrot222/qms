from models.db import get_db_connection
import mysql.connector
from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/estimated_wait_time')
def estimated_wait_time():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})

    try:
        cursor = conn.cursor(dictionary=True)

        # Use backticks for column alias to avoid SQL syntax issues
        query = "SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(ETR)) + AVG(TIME_TO_SEC(ETR))) AS EstimatedWaitTimeFROM walkin;"
        cursor.execute(query)

        result = cursor.fetchone()   # Only one row, so fetchone() is better than fetchall()
        cursor.close()
        conn.close()

        # Extract the numeric value cleanly
        estimated_time = result.get('EstimatedWaitTime') if result else "00:00:00"

        return jsonify({
            "success": True,
            "estimated_wait_time": estimated_time
        })

    except mysql.connector.Error as e:
        return jsonify({"success": False, "error": f"Database error: {str(e)}"})

    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"})
