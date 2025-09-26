from flask import Flask, render_template
from dotenv import load_dotenv
import os
import mysql.connector

# Load the .env file
load_dotenv()

app = Flask(__name__)

# Access values from .env
app.secret_key = os.getenv("SECRET_KEY")
port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set in the .env

try:
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    print('Database connected successfully.')
except mysql.connector.Error as e:
    print(f"Database connection failed: {e}")
    conn = None  # Avoid crashing if DB is not connected

@app.route("/")
# Home Page
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/status")
def status():
    return render_template("status.html")

if __name__ == "__main__":
    # Run the app on the port from .env or default to 5000
    app.run(debug=True, port=port)
