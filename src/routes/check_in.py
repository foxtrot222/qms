from flask import Blueprint, request, jsonify, session
from models.db import get_db_connection
from math import radians, sin, cos, sqrt, atan2

check_in_bp = Blueprint('check_in', __name__)

def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

@check_in_bp.route('/check_in', methods=['POST'])
def check_in():
    data = request.get_json()
    user_lat = data.get('latitude')
    user_lon = data.get('longitude')

    if not user_lat or not user_lon:
        return jsonify({"success": False, "error": "Location data is required."})

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Assuming one organization, fetch its location
        cursor.execute("SELECT latitude, longitude, factor FROM admin ORDER BY id LIMIT 1")
        org = cursor.fetchone()
        if not org or not org['latitude'] or not org['longitude']:
            return jsonify({"success": False, "error": "Organization location not configured."})

        distance = haversine(user_lat, user_lon, org['latitude'], org['longitude'])
        
        # factor is the vicinity radius in kilometers
        vicinity = org['factor'] if org['factor'] else 0.5 # default 500 meters

        if distance <= vicinity:
            # Here you could also update the database to mark the user as checked-in
            return jsonify({"success": True, "message": "Check-in successful!"})
        else:
            return jsonify({"success": False, "error": f"You are too far from the location. Distance: {distance:.2f} km"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()
