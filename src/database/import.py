import os
import sys
import shutil
import subprocess
from dotenv import load_dotenv

# -----------------------------
# Load .env
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "../../.env")
load_dotenv(ENV_PATH)

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

if not DB_USER or not DB_PASS or not DB_NAME:
    print("❌ Missing DB_USER, DB_PASS, or DB_NAME in .env file.")
    sys.exit(1)

# -----------------------------
# Files
# -----------------------------
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")
DATA_FILE = os.path.join(BASE_DIR, "data.sql")

# -----------------------------
# Locate mysql
# -----------------------------
MYSQL_CMD = shutil.which("mysql")
if not MYSQL_CMD:
    # fallback Windows default path
    if os.name == "nt":
        MYSQL_CMD = r"C:/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe"
    else:
        print("❌ 'mysql' command not found in PATH.")
        sys.exit(1)

# -----------------------------
# Import functions
# -----------------------------
def import_file(file_path):
    if not os.path.exists(file_path):
        print(f"⚠️  File {file_path} not found. Skipping.")
        return

    try:
        subprocess.run(
            [MYSQL_CMD, f"-u{DB_USER}", f"-p{DB_PASS}", DB_NAME],
            stdin=open(file_path, "r"),
            check=True
        )
        print(f"✅ Imported {file_path}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to import {file_path}")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting database import...")
    import_file(SCHEMA_FILE)
    import_file(DATA_FILE)
    print("🏁 Import script finished.")
