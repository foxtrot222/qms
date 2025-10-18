from flask import Blueprint,render_template,flash,redirect,url_for,session,request,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.db import get_db_connection
import mysql.connector
import time

admin_bp=Blueprint('admin',__name__)

# ... (existing routes)

@admin_bp.route('/admin/users/add', methods=['POST'])
def add_user():
    name = request.form.get('name')
    officer_id = request.form.get('officerID')
    password = request.form.get('password')
    service_id = request.form.get('service_id')

    if not all([name, officer_id, password, service_id]):
        flash("All fields are required to add a user.", "error")
        return redirect(url_for('admin.admin'))

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO service_provider (name, officerID, password, service_id) VALUES (%s, %s, %s, %s)",
            (name, officer_id, hashed_password, service_id)
        )
        conn.commit()
        flash(f"User {name} added successfully!", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Failed to add user: {e}", "error")
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in add_user(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/users/revoke/<int:user_id>')
def revoke_user(user_id):
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE service_provider SET service_id = 0 WHERE id = %s", (user_id,))
        conn.commit()
        flash(f"User {user_id} revoked successfully!", "success")
    except mysql.connector.Error as e:
        conn.rollback()
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in revoke_user(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/users/<int:user_id>/get', methods=['GET'])
def get_user_data(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, officerID, service_id FROM service_provider WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return jsonify({"success": True, "user": user})
        else:
            return jsonify({"success": False, "error": "User not found."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@admin_bp.route('/admin/users/update', methods=['POST'])
def update_user():
    user_id = request.form.get('id')
    name = request.form.get('name')
    officer_id = request.form.get('officerID')
    service_id = request.form.get('service_id')
    password = request.form.get('password') # Get the new password

    if not all([user_id, name, officer_id, service_id]):
        flash("All fields are required to update a user (except password).", "error")
        return redirect(url_for('admin.admin'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        update_query = "UPDATE service_provider SET name = %s, officerID = %s, service_id = %s"
        params = [name, officer_id, service_id]

        if password: # If a new password is provided, hash and include it in the update
            hashed_password = generate_password_hash(password)
            update_query += ", password = %s"
            params.append(hashed_password)
        
        update_query += " WHERE id = %s"
        params.append(user_id)

        cursor.execute(update_query, tuple(params))
        conn.commit()
        flash(f"User {name} updated successfully!", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Failed to update user: {e}", "error")
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in update_user(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/users/edit/<int:user_id>')
def edit_user(user_id):
    flash(f"Edit user {user_id} - functionality not yet implemented.", "info")
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/users/delete/<int:user_id>')
def delete_user(user_id):
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM service_provider WHERE id = %s", (user_id,))
        conn.commit()
        flash(f"User {user_id} deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in delete_user(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/services/delete/<int:service_id>')
def delete_service(service_id):
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        # Get the service name before deleting the service entry
        cursor.execute("SELECT name FROM service WHERE id = %s", (service_id,))
        service_name_result = cursor.fetchone()

        if service_name_result:
            service_name = service_name_result[0] # Access by index
            service_table_name = service_name

            # Before deleting the service, update any service_providers associated with it
            cursor.execute("UPDATE service_provider SET service_id = 0 WHERE service_id = %s", (service_id,))
            cursor.execute("DELETE FROM service WHERE id = %s", (service_id,))
            conn.commit()

            # Drop the corresponding service queue table
            drop_table_sql = f"DROP TABLE IF EXISTS `{service_table_name}`"
            cursor.execute(drop_table_sql)
            conn.commit()

            flash(f"Service {service_name} deleted successfully and table '{service_table_name}' dropped!", "success")
        else:
            flash(f"Service with ID {service_id} not found.", "error")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Failed to delete service: {e}", "error")
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in delete_service(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/services/<int:service_id>/get', methods=['GET'])
def get_service_data(service_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM service WHERE id = %s", (service_id,))
        service = cursor.fetchone()
        if service:
            return jsonify({"success": True, "service": service})
        else:
            return jsonify({"success": False, "error": "Service not found."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@admin_bp.route('/admin/services/update', methods=['POST'])
def update_service():
    service_id = request.form.get('id')
    service_name = request.form.get('name')

    if not all([service_id, service_name]):
        flash("Service ID and name are required to update a service.", "error")
        return redirect(url_for('admin.admin'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE service SET name = %s WHERE id = %s",
            (service_name, service_id)
        )
        conn.commit()
        flash(f"Service {service_name} updated successfully!", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Failed to update service: {e}", "error")
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in update_service(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/services/edit/<int:service_id>')
def edit_service(service_id):
    flash(f"Edit service {service_id} - functionality not yet implemented.", "info")
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/services/add', methods=['POST'])
def add_service():
    service_name = request.form.get('name')

    if not service_name:
        flash("Service name is required to add a service.", "error")
        return redirect(url_for('admin.admin'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO service (name) VALUES (%s)", (service_name,))
        conn.commit()

        # Create a new table for the service queue
        service_table_name = service_name
        create_table_sql = f"""CREATE TABLE `{service_table_name}` (
            `id` int unsigned NOT NULL AUTO_INCREMENT,
            `position` tinyint unsigned NOT NULL,
            `token_id` int unsigned NOT NULL,
            `ETR` time DEFAULT NULL,
            `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            KEY `fk_token` (`token_id`),
            CONSTRAINT `fk_{service_table_name}_token` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"""
        cursor.execute(create_table_sql)
        conn.commit()

        flash(f"Service '{service_name}' added successfully and table '{service_table_name}' created!", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Failed to add service: {e}", "error")
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in add_service(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin')
def admin():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return render_template('admin.html', stats=None)

    try:
        cursor = conn.cursor(dictionary=True)

        # 1. Active Officers
        cursor.execute("SELECT COUNT(*) as count FROM service_provider")
        active_officers = cursor.fetchone()['count']

        # Get all service tables
        cursor.execute("SELECT name FROM service")
        services = cursor.fetchall()
        service_tables = [service['name'] for service in services]

        # 2. Customers Waiting & 3. Avg. Wait Time
        total_waiting = 0
        total_etr_seconds = 0

        for table in service_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) as count, SUM(TIME_TO_SEC(ETR)) FROM {table} WHERE position > 0")
                result = cursor.fetchone()
                if result:
                    total_waiting += result.get('count', 0)
                    if result.get('total_etr'):
                        total_etr_seconds += float(result['total_etr'])
            except mysql.connector.Error:
                # Table might not exist, ignore.
                pass

        cursor.execute("SELECT factor, latitude, longitude FROM admin ORDER BY id LIMIT 1")
        admin_settings = cursor.fetchone()
        lateness_factor = admin_settings['factor'] if admin_settings else 0.5
        latitude = admin_settings['latitude'] if admin_settings else 0.0
        longitude = admin_settings['longitude'] if admin_settings else 0.0

        # Get avg service time from logs, similar to get_dashboard_stats
        cursor.execute("SELECT TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(log))), '%i:%s') as avg_time FROM logs")
        avg_time_result = cursor.fetchone()
        avg_wait_time = avg_time_result['avg_time'] if avg_time_result['avg_time'] else "00:00"

        stats = {
            'active_officers': active_officers,
            'customers_waiting': total_waiting,
            'avg_wait_time': avg_wait_time,
            'lateness_factor': lateness_factor,
            'latitude': latitude,
            'longitude': longitude
        }

        # Fetch users (service providers)
        cursor.execute("SELECT id, name, officerID, service_id FROM service_provider")
        users = cursor.fetchall()

        # Fetch services
        cursor.execute("SELECT id, name FROM service")
        services = cursor.fetchall()

        # Fetch consumers
        cursor.execute("SELECT consumer_id, email_id FROM consumer")
        consumers = cursor.fetchall()

        return render_template('admin.html', stats=stats, users=users, services=services, consumers=consumers)

    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return render_template('admin.html', stats=None)
        return render_template('admin.html', stats=None)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@admin_bp.route('/adminlogin',methods=['POST'])
def admin_login():
    conn=get_db_connection()
    if not conn:
        flash("Database connection failed. Please try again later.")
        return redirect(url_for("admin.login"))
    adminId=request.form.get('adminID')
    adminPassword=request.form.get('adminPassword')
    if not adminId or not adminPassword:
        return jsonify({"success": False, "error": "Provide both ID and password."})

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE name=%s", (adminId,))
        admin = cursor.fetchone()
        if admin and check_password_hash(admin['password'], adminPassword):
            cursor.close()

            session['admin_id'] = admin['id']
            session['adminname'] = admin['name']
            return jsonify({"success": True, "redirect": "/admin"})
        else:
            cursor.close()
            return jsonify({"success": False, "error": "Invalid ID or password."})

    except mysql.connector.Error as err:
        print("Database query failed:", err)
        return jsonify({"success": False, "error": "Database error occurred."})

@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('adminname', None)
    return redirect(url_for('org.organization'))

@admin_bp.route('/admin/settings/update', methods=['POST'])
def update_settings():
    new_factor = request.form.get('lateness_factor')
    new_latitude = request.form.get('latitude')
    new_longitude = request.form.get('longitude')

    if new_factor is None or new_latitude is None or new_longitude is None:
        flash("Missing form data.", "error")
        return redirect(url_for('admin.admin'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        # Updates the settings for the first admin entry.
        cursor.execute("UPDATE admin SET factor = %s, latitude = %s, longitude = %s ORDER BY id LIMIT 1", (float(new_factor), float(new_latitude), float(new_longitude)))
        conn.commit()
        flash("Settings updated successfully!", "success")
    except Exception as e:
        conn.rollback()
        print(f"An unexpected error occurred in update_settings(): {e}")
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/consumers/add', methods=['POST'])
def add_consumer():
    consumer_id = request.form.get('consumer_id')
    email_id = request.form.get('email_id')

    if not all([consumer_id, email_id]):
        flash("Consumer ID and Email are required.", "error")
        return redirect(url_for('admin.admin'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO consumer (consumer_id, email_id) VALUES (%s, %s)",
            (consumer_id, email_id)
        )
        conn.commit()
        flash(f"Consumer {consumer_id} added successfully!", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Failed to add consumer: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/consumers/update', methods=['POST'])
def update_consumer():
    original_consumer_id = request.form.get('original_consumer_id')
    consumer_id = request.form.get('consumer_id')
    email_id = request.form.get('email_id')

    if not all([original_consumer_id, consumer_id, email_id]):
        flash("All fields are required to update a consumer.", "error")
        return redirect(url_for('admin.admin'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE consumer SET consumer_id = %s, email_id = %s WHERE consumer_id = %s",
            (consumer_id, email_id, original_consumer_id)
        )
        conn.commit()
        flash(f"Consumer {consumer_id} updated successfully!", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Failed to update consumer: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/consumers/delete/<consumer_id>')
def delete_consumer(consumer_id):
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for('admin.admin'))

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consumer WHERE consumer_id = %s", (consumer_id,))
        conn.commit()
        flash(f"Consumer {consumer_id} deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"An unexpected error occurred: {e}", "error")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/consumers/<consumer_id>/get', methods=['GET'])
def get_consumer_data(consumer_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed."})
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT consumer_id, email_id FROM consumer WHERE consumer_id = %s", (consumer_id,))
        consumer = cursor.fetchone()
        if consumer:
            return jsonify({"success": True, "consumer": consumer})
        else:
            return jsonify({"success": False, "error": "Consumer not found."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()