from flask import Blueprint, request , jsonify ,session
from models.db import get_db_connection
import mysql.connector
import time
import logging
service_provider_bp=Blueprint("service_provider",__name__)

@service_provider_bp.route("/get_queue")
def get_queue():
    logging.info("Attempting to fetch queue data.")
    table_name = session.get('table_name')
    if not table_name:
        logging.error("No table name in session.")
        return jsonify({"success": False, "error": "User not associated with a valid service."})

    try:
        conn = get_db_connection()
        if not conn:
            logging.error("Database connection failed.")
            return jsonify({"success": False, "error": "Database connection failed."})
        
        logging.info(f"Database connection successful. Executing query on table: {table_name}")
        cursor = conn.cursor(dictionary=True)
        
        query = f"""
            SELECT
                q.position,
                t.value AS token_value
            FROM
                {table_name} q
            JOIN
                token t ON q.token_id = t.id
            ORDER BY
                q.position;
        """
        cursor.execute(query)
        queue = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info(f"Found {len(queue)} customers in the {table_name} queue.")

        return jsonify({"success": True, "queue": queue})

    except mysql.connector.Error as err:
        logging.error(f"Database query failed: {err}")
        return jsonify({"success": False, "error": "Database error occurred."})
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"success": False, "error": "An unexpected error occurred."})


@service_provider_bp.route("/complete_service", methods=['POST'])
def complete_service():
    logging.info("Attempting to complete a service.")
    table_name = session.get('table_name')
    if not table_name:
        logging.error("No table name in session for complete_service.")
        return jsonify({"success": False, "error": "User not associated with a valid service."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        service_time_seconds = int(request.form.get('service_time', 0))
        if service_time_seconds > 1: # Log only realistic times
            service_time_formatted = time.strftime('%H:%M:%S', time.gmtime(service_time_seconds))
            cursor.execute("INSERT INTO logs (log) VALUES (%s)", (service_time_formatted,))

        # Find the customer being served from the correct table
        cursor.execute(f"SELECT token_id FROM {table_name} WHERE position = 0 LIMIT 1")
        serving = cursor.fetchone()

        if serving:
            token_id_to_delete = serving['token_id']
            # Remove from the service queue table
            cursor.execute(f"DELETE FROM {table_name} WHERE token_id = %s", (token_id_to_delete,))
            # Also remove from appointment if they had one
            cursor.execute("UPDATE appointment SET is_booked = 0, token_id = NULL WHERE token_id = %s", (token_id_to_delete,))
            # Now delete the token, which should cascade to customer
            cursor.execute("DELETE FROM token WHERE id = %s", (token_id_to_delete,))

        # Shift the entire queue for the specific service up
        cursor.execute(f"UPDATE {table_name} SET position = position - 1 WHERE position > 0")

        # Recalculate all ETRs for the remaining queue
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time = float(avg_time_result['avg_time'] or 180)

        cursor.execute(f"SELECT id, position FROM {table_name} ORDER BY position")
        remaining_queue = cursor.fetchall()

        for person in remaining_queue:
            etr_in_seconds = person['position'] * avg_service_time
            etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))
            cursor.execute(f"UPDATE {table_name} SET ETR = %s WHERE id = %s", (etr_formatted, person['id']))

        conn.commit()

    except Exception as e:
        conn.rollback()
        logging.error(f"An unexpected error occurred in complete_service: {e}")
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True})