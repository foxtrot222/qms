import mysql.connector
import os

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),  # Use TCP/IP, not named pipe
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", ""),
            database=os.getenv("DB_NAME", "qms_db"),
            port=int(os.getenv("DB_PORT", 3306)),     # Ensure port is included
            unix_socket=None,                         # Disable named pipes
            connection_timeout=10
        )
        print("✅ Database connected successfully!")
        return conn
    except mysql.connector.Error as e:
        print("❌ Database connection failed:", e)
        return None
