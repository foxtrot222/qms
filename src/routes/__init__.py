from .token import token_bp
from .otp import otp_bp
from .status import status_bp
from .appointment import appointment_bp
from .service_provider import service_provider_bp
from .main import main_bp
from .organization import org_bp
from .auth import auth_bp
from .check_in import check_in_bp
from .admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(token_bp)
    app.register_blueprint(otp_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(service_provider_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(check_in_bp)

def org_register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(service_provider_bp)
    app.register_blueprint(org_bp)