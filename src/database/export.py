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
# Output files
# -----------------------------
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")
DATA_FILE = os.path.join(BASE_DIR, "data.sql")

# -----------------------------
# Locate mysqldump
# -----------------------------
MYSQLDUMP_CMD = shutil.which("mysqldump")
if not MYSQLDUMP_CMD:
    # fallback Windows default path
    if os.name == "nt":
        MYSQLDUMP_CMD = r"C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe"
    else:
        print("❌ 'mysqldump' command not found in PATH.")
        sys.exit(1)

# -----------------------------
# Export functions
# -----------------------------
def export_file(args, output_file):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            subprocess.run(
                [MYSQLDUMP_CMD] + args,
                stdout=f,
                check=True
            )
        print(f"✅ Exported to {output_file}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to export to {output_file}")

def export_schema():
    """Export only schema (no data)"""
    args = [f"-u{DB_USER}", f"-p{DB_PASS}", "--no-data", DB_NAME]
    export_file(args, SCHEMA_FILE)

def export_data():
    """Export only data (no schema)"""
    args = [f"-u{DB_USER}", f"-p{DB_PASS}", "--no-create-info", DB_NAME]
    export_file(args, DATA_FILE)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting database export...")
    export_schema()
    export_data()
    print("🏁 Export script finished.")
