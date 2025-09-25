from flask import Flask, render_template
from dotenv import load_dotenv
import os
import mysql.connector
# Load the .env file
load_dotenv()
app = Flask(__name__)
# Access values from .env
app.secret_key = os.getenv("SECRET_KEY")
try:
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    print('Database connected successfuly.')
except mysql.connector.Error as e:
    print(f"Database connection failed: {e}")
    conn = None  # Avoid crashing if DB is not connected
@app.route("/")
#Home Page
def home():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
