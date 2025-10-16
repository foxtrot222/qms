"""
Authentication decorators for protecting routes
"""
from functools import wraps
from flask import session, jsonify, redirect, url_for, flash

def login_required(f):
    """
    Decorator to require service provider authentication
    Use: @login_required above route functions
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # For JSON APIs
            if '/api/' in str(f.__name__) or 'json' in str(f.__name__):
                return jsonify({"success": False, "error": "Authentication required"}), 401
            # For HTML pages
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('org.organization'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin authentication
    Use: @admin_required above route functions
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            # For JSON APIs
            if '/api/' in str(f.__name__) or 'json' in str(f.__name__):
                return jsonify({"success": False, "error": "Admin authentication required"}), 401
            # For HTML pages
            flash("Admin access required.", "warning")
            return redirect(url_for('org.organization'))
        return f(*args, **kwargs)
    return decorated_function

def token_verified(f):
    """
    Decorator to require OTP-verified token in session
    Use: @token_verified above route functions
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'verified_token' not in session:
            return jsonify({"success": False, "error": "Token verification required"}), 401
        return f(*args, **kwargs)
    return decorated_function
