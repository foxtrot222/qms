from flask import Flask
from dotenv import load_dotenv
import os
from routes import register_blueprints
# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")
port = int(os.getenv("PORT", 5000))
register_blueprints(app)

# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
