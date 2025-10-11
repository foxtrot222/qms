from flask import Blueprint,render_template,flash,redirect,url_for,session,request,jsonify
from werkzeug.security import check_password_hash
from models.db import get_db_connection
import mysql.connector

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/admin')
def admin():
    return render_template('admin.html')

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
        if admin and (admin['password']== adminPassword):
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