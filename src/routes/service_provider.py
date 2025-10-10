from flask import Blueprint,render_template , request , redirect ,url_for ,flash, jsonify ,session
from models.db import get_db_connection
import mysql.connector
import time
import logging
service_provider_bp=Blueprint("service_provider",__name__)

@service_provider_bp.route("/get_queue")
def get_queue():
    logging.info("Attempting to fetch queue data.")
    try:
        conn = get_db_connection()
        if not conn:
            logging.error("Database connection failed.")
            return jsonify({"success": False, "error": "Database connection failed."})
        
        logging.info("Database connection successful. Executing query.")
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
                w.position,
                t.value AS token_value
            FROM
                walkin w
            JOIN
                token t ON w.token_id = t.id
            ORDER BY
                w.position;
        """
        cursor.execute(query)
        queue = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info(f"Found {len(queue)} customers in the queue.")

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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        service_time_seconds = int(request.form.get('service_time', 0))
        if service_time_seconds > 1: # Log only realistic times
            service_time_formatted = time.strftime('%H:%M:%S', time.gmtime(service_time_seconds))
            cursor.execute("INSERT INTO logs (log) VALUES (%s)", (service_time_formatted,))

        # Find the customer being served
        cursor.execute("SELECT token_id FROM walkin WHERE position = 0 LIMIT 1")
        serving = cursor.fetchone()

        if serving:
            token_id_to_delete = serving['token_id']
            # Remove references from child tables first
            cursor.execute("DELETE FROM walkin WHERE token_id = %s", (token_id_to_delete,))
            cursor.execute("UPDATE appointment SET is_booked = 0, token_id = NULL WHERE token_id = %s", (token_id_to_delete,))
            # Now delete the token, which should cascade to customer
            cursor.execute("DELETE FROM token WHERE id = %s", (token_id_to_delete,))

        # Shift the entire queue up
        cursor.execute("UPDATE walkin SET position = position - 1 WHERE position > 0")

        # Recalculate all ETRs for the remaining queue
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time_decimal = avg_time_result['avg_time'] if avg_time_result['avg_time'] and avg_time_result['avg_time'] > 0 else 180
        avg_service_time = float(avg_service_time_decimal)

        cursor.execute("SELECT id, position FROM walkin ORDER BY position")
        remaining_queue = cursor.fetchall()

        for person in remaining_queue:
            etr_in_seconds = person['position'] * avg_service_time
            etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))
            cursor.execute("UPDATE walkin SET ETR = %s WHERE id = %s", (etr_formatted, person['id']))

        conn.commit()

    except Exception as e:
        conn.rollback()
        logging.error(f"An unexpected error occurred in complete_service: {e}")
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True})
