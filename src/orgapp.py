from flask import Flask
from dotenv import load_dotenv
import os
import socket
from routes import org_register_blueprints

# ------------------- Load Environment Variables -------------------
load_dotenv()

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'org_session'
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# ------------------- Get Port or Find Next Available -------------------
def get_available_port(start_port=5000, max_tries=10):
    """Find the next available port starting from start_port."""
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port  # Found an available port
            except OSError:
                port += 1  # Try next port
    raise OSError(f"No available port found from {start_port} to {port - 1}")

# Try to get PORT from .env, else start from 5000
start_port = int(os.getenv("PORT", 5000))
port = get_available_port(start_port)

# ------------------- Register Blueprints -------------------
org_register_blueprints(app)

@app.route('/debug-routes')
def debug_routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(f"Endpoint: {rule.endpoint}, Methods: {','.join(rule.methods)}, Rule: {rule.rule}")
    return "<pre>" + "\n".join(output) + "</pre>"

# ------------------- Run App -------------------
if __name__ == "__main__":
    print(f"Running Flask app on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
