from flask import Blueprint , request , jsonify
from models.db import get_db_connection
import time
appointment_bp=Blueprint('appointment',__name__)

@appointment_bp.route('/get_available_slots', methods=['GET'])
def get_available_slots():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, TIME_FORMAT(time_slot, '%h:%i %p') as time_slot FROM appointment WHERE is_booked = 0 ORDER BY time_slot")
    slots = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "slots": slots})

@appointment_bp.route('/join_walkin', methods=['POST'])
def join_walkin():
    data = request.get_json()
    token_value = data.get('token')
    if not token_value:
        return jsonify({"success": False, "error": "Token is required."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, type FROM token WHERE value = %s", (token_value,))
        token_record = cursor.fetchone()
        if not token_record:
            return jsonify({"success": False, "error": "Invalid token."})
        
        token_id = token_record['id']
        service_id = int(token_record['type'])

        # Get table name from service id
        cursor.execute("SELECT name FROM service WHERE id = %s", (service_id,))
        service_record = cursor.fetchone()
        if not service_record:
            return jsonify({"success": False, "error": "Invalid service for token."})
        
        table_name = service_record['name'].lower()

        if not table_name:
            return jsonify({"success": False, "error": "Invalid service type for token."})

        # Calculate average service time from logs (defaults to 3 minutes if no logs)
        cursor.execute("SELECT AVG(TIME_TO_SEC(log)) as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_service_time_decimal = avg_time_result['avg_time'] if avg_time_result['avg_time'] else 180
        avg_service_time = float(avg_service_time_decimal)

        # Determine position in the specific queue
        cursor.execute(f"SELECT id FROM {table_name} WHERE position = 0")
        serving_now = cursor.fetchone()
        if not serving_now:
            next_pos = 0
        else:
            cursor.execute(f"SELECT MAX(position) as max_pos FROM {table_name}")
            max_pos_record = cursor.fetchone()
            next_pos = (max_pos_record['max_pos'] or 0) + 1

        # Calculate ETR
        etr_in_seconds = next_pos * avg_service_time
        etr_formatted = time.strftime('%H:%M:%S', time.gmtime(etr_in_seconds))

        # Insert into the specific service table
        cursor.execute(f"INSERT INTO {table_name} (token_id, position, ETR) VALUES (%s, %s, %s)", (token_id, next_pos, etr_formatted))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True, "message": "Successfully joined walk-in queue."})

@appointment_bp.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.get_json()
    token_value = data.get('token')
    slot_id = data.get('slot_id')
    if not token_value or not slot_id:
        return jsonify({"success": False, "error": "Token and slot are required."})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM token WHERE value = %s", (token_value,))
        token_record = cursor.fetchone()
        if not token_record:
            return jsonify({"success": False, "error": "Invalid token."})
        token_id = token_record['id']

        cursor.execute("SELECT is_booked FROM appointment WHERE id = %s FOR UPDATE", (slot_id,))
        slot_record = cursor.fetchone()
        if not slot_record:
            return jsonify({"success": False, "error": "Invalid slot."})
        if slot_record['is_booked']:
            conn.rollback()
            return jsonify({"success": False, "error": "Slot already taken."})
        
        cursor.execute("UPDATE appointment SET is_booked = 1, token_id = %s WHERE id = %s", (token_id, slot_id))
        cursor.execute("UPDATE token SET type = 'appointment' WHERE id = %s", (token_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True, "message": "Appointment booked successfully."})