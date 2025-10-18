from flask import Blueprint, request , jsonify ,session
from models.db import get_db_connection
import mysql.connector
import time
import logging
from utils.email_utils import send_completion_email

service_provider_bp=Blueprint("service_provider",__name__)


@service_provider_bp.route("/get_queue")
def get_queue():
    logging.info("Attempting to fetch queue data.")
    table_name = session.get('table_name')
    if not table_name:
        return jsonify({"success": False, "error": "User not associated with a valid service."})

    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "error": "Database connection failed."})
        
        cursor = conn.cursor(dictionary=True)
        
        query = f"""
            SELECT
                q.position,
                t.id AS token_id,
                t.value AS token_value,
                c.name AS customer_name,
                c.email AS customer_email
            FROM
                {table_name} q
            JOIN
                token t ON q.token_id = t.id
            JOIN
                customer c ON t.customer_id = c.id
            ORDER BY
                q.position;
        """
        cursor.execute(query)
        queue = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "queue": queue})

    except Exception as e:
        logging.error(f"An unexpected error occurred in get_queue: {e}")
        return jsonify({"success": False, "error": "An unexpected error occurred."})

@service_provider_bp.route("/get_dashboard_stats")
def get_dashboard_stats():
    table_name = session.get('table_name')
    if not table_name:
        return jsonify({"success": False, "error": "User not associated with a valid service."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get queue length (customers in line, not including the one being served)
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name} WHERE position > 0")
        customer_count = cursor.fetchone()['count']

        # Get avg service time
        cursor.execute("SELECT TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(log))), '%i:%s') as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_time = avg_time_result['avg_time'] if avg_time_result['avg_time'] else "00:00"

        cursor.close()
        conn.close()
        return jsonify({
            "success": True,
            "stats": {
                "customer_count": customer_count,
                "avg_time": avg_time
            }
        })
    except Exception as e:
        logging.error(f"An unexpected error occurred in get_dashboard_stats: {e}")
        return jsonify({"success": False, "error": str(e)})

@service_provider_bp.route("/complete_service", methods=['POST'])
def complete_service():
    logging.info("Attempting to complete a service.")
    table_name = session.get('table_name')
    if not table_name:
        return jsonify({"success": False, "error": "User not associated with a valid service."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        service_time_seconds = int(request.form.get('service_time', 0))
        service_time_formatted = time.strftime('%H:%M:%S', time.gmtime(service_time_seconds))
        if service_time_seconds > 1: # Log only realistic times
            cursor.execute("INSERT INTO logs (log) VALUES (%s)", (service_time_formatted,))

        # Find and delete the customer being served
        cursor.execute(f"SELECT token_id FROM {table_name} WHERE position = 0 LIMIT 1")
        serving = cursor.fetchone()

        if serving:
            token_id_to_delete = serving['token_id']
            
            cursor.execute("SELECT email FROM customer WHERE token_id = %s", (token_id_to_delete,))
            customer_email_record = cursor.fetchone()
            customer_email = customer_email_record['email'] if customer_email_record else None

            cursor.execute(f"DELETE FROM {table_name} WHERE token_id = %s", (token_id_to_delete,))
            cursor.execute("UPDATE appointment SET is_booked = 0, token_id = NULL WHERE token_id = %s", (token_id_to_delete,))
            cursor.execute("DELETE FROM token WHERE id = %s", (token_id_to_delete,))
        
        conn.commit()

        if serving and customer_email:
            send_completion_email(customer_email, service_time_formatted)

    except Exception as e:
        conn.rollback()
        logging.error(f"An unexpected error occurred in complete_service: {e}")
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True})

@service_provider_bp.route("/call_next", methods=['POST'])
def call_next():
    logging.info("Attempting to call next customer.")
    table_name = session.get('table_name')
    if not table_name:
        return jsonify({"success": False, "error": "User not associated with a valid service."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Shift the entire queue up
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
        logging.error(f"An unexpected error occurred in call_next: {e}")
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True})

@service_provider_bp.route("/mark_late", methods=["POST"])
def mark_late():
    data = request.get_json()
    token_id = data.get("token_id")
    table_name = session.get('table_name')

    if not table_name or not token_id:
        return jsonify({"success": False, "error": "Missing required data."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get Lateness Factor (W_L)
        cursor.execute("SELECT factor FROM admin ORDER BY id LIMIT 1")
        admin_config = cursor.fetchone()
        factor = admin_config.get('factor') if admin_config else None
        w_l = float(factor) if factor is not None else 0.5

        # Get Queue Length (N_queue) - number of people waiting
        cursor.execute(f"SELECT COUNT(*) as n_queue FROM {table_name} WHERE position > 0")
        n_queue = cursor.fetchone()['n_queue']

        # Calculate New Position using the formula P_new = 1 + W_L * N_queue
        new_pos = round(1 + w_l * n_queue)

        # Cap new_pos to be at the end of the line (position n_queue)
        if new_pos > n_queue:
            new_pos = n_queue

        # Get the token_id of the customer at position 0 to ensure it matches
        cursor.execute(f"SELECT token_id FROM {table_name} WHERE position = 0 LIMIT 1")
        late_customer = cursor.fetchone()
        if not late_customer or late_customer['token_id'] != token_id:
            return jsonify({"success": False, "error": "Token mismatch or no customer being served."})
        
        # Update positions atomically using a CASE statement
        update_query = f"""
            UPDATE {table_name}
            SET position = CASE
                WHEN token_id = %s THEN %s
                WHEN position > 0 AND position <= %s THEN position - 1
                ELSE position
            END
        """
        cursor.execute(update_query, (token_id, new_pos, new_pos))

        # Recalculate all ETRs for the updated queue
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time = float(avg_time_result['avg_time'] or 180)

        cursor.execute(f"SELECT id, position FROM {table_name} ORDER BY position")
        full_queue = cursor.fetchall()

        for person in full_queue:
            etr_in_seconds = person['position'] * avg_service_time
            etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))
            cursor.execute(f"UPDATE {table_name} SET ETR = %s WHERE id = %s", (etr_formatted, person['id']))

        conn.commit()

        return jsonify({"success": True, "new_position": new_pos})

    except Exception as e:
        conn.rollback()
        logging.error(f"An unexpected error occurred in mark_late: {e}")
        return jsonify({"success": False, "error": "Database error occurred."})

    finally:
        cursor.close()
        conn.close()

@service_provider_bp.route("/get_transfer_services")
def get_transfer_services():
    service_id = session.get('service_id')
    if not service_id:
        return jsonify({"success": False, "error": "User not associated with a valid service."})

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM service WHERE id != %s ORDER BY name", (service_id,))
        services = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "services": services})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@service_provider_bp.route("/transfer_customer", methods=['POST'])
def transfer_customer():
    destination_service_id = request.json.get('destination_service_id')
    source_table_name = session.get('table_name')

    if not destination_service_id or not source_table_name:
        return jsonify({"success": False, "error": "Missing required data for transfer."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get the token of the customer being served
        cursor.execute(f"SELECT token_id FROM {source_table_name} WHERE position = 0 LIMIT 1")
        serving = cursor.fetchone()
        if not serving:
            return jsonify({"success": False, "error": "No customer is currently being served."})
        
        token_id_to_transfer = serving['token_id']

        # Get destination table name
        cursor.execute("SELECT name FROM service WHERE id = %s", (destination_service_id,))
        service_record = cursor.fetchone()
        if not service_record:
            return jsonify({"success": False, "error": "Invalid destination service."})
        destination_table_name = service_record['name']

        # Start transaction
        # 1. Delete from source table
        cursor.execute(f"DELETE FROM {source_table_name} WHERE token_id = %s", (token_id_to_transfer,))

        # 2. Update customer's service_id and token type
        cursor.execute("UPDATE customer c JOIN token t ON c.token_id = t.id SET c.service_id = %s WHERE t.id = %s", (destination_service_id, token_id_to_transfer))
        cursor.execute("UPDATE token SET type = %s WHERE id = %s", (destination_service_id, token_id_to_transfer))

        # 3. Insert into destination table
        # Calculate average service time for the destination queue (or global)
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time = float(avg_time_result['avg_time'] or 180)

        # Determine next position in the destination queue
        cursor.execute(f"SELECT COUNT(*) as queue_length FROM {destination_table_name}")
        queue_length = cursor.fetchone()['queue_length']
        next_pos = queue_length

        # Calculate ETR for the new person
        etr_in_seconds = next_pos * avg_service_time
        etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))

        cursor.execute(f"INSERT INTO {destination_table_name} (token_id, position, ETR) VALUES (%s, %s, %s)", (token_id_to_transfer, next_pos, etr_formatted))

        conn.commit()
        
    except Exception as e:
        conn.rollback()
        logging.error(f"An unexpected error occurred during transfer: {e}")
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True, "message": "Customer transferred successfully."})
