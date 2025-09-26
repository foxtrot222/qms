import os
import sys
import shutil
import subprocess
from dotenv import load_dotenv  # For reading environment variables from a .env file

# -----------------------------
# Load .env file
# -----------------------------
# Determine the directory where this script resides
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct path to the .env file (two levels up from script location)
ENV_PATH = os.path.join(BASE_DIR, "../../.env")

# Load environment variables from the .env file
load_dotenv(ENV_PATH)

# Read DB credentials from environment
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# If any of the required environment variables are missing, exit the script
if not DB_USER or not DB_PASS or not DB_NAME:
    print("Missing DB_USER, DB_PASS, or DB_NAME in .env file.")
    sys.exit(1)

# -----------------------------
# Output file paths
# -----------------------------
# SQL file to store database schema only (tables, indexes, etc.)
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")

# SQL file to store database data only (INSERT statements)
DATA_FILE = os.path.join(BASE_DIR, "data.sql")

# -----------------------------
# Locate mysqldump executable
# -----------------------------
# Try to find 'mysqldump' in system PATH
MYSQLDUMP_CMD = shutil.which("mysqldump")

# If not found, check default Windows installation path
if not MYSQLDUMP_CMD:
    if os.name == "nt":  # Windows
        MYSQLDUMP_CMD = r"C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe"
    else:
        print("'mysqldump' command not found in PATH.")
        sys.exit(1)

# -----------------------------
# Export functions
# -----------------------------

def import_file(args, output_file):
    """
    Run mysqldump with the given arguments and save the output to a file.
    Shows detailed error messages if something goes wrong.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            result = subprocess.run(
                [MYSQLDUMP_CMD] + args,   # Full command: mysqldump + args
                stdout=f,                 # Dump output -> file
                stderr=subprocess.PIPE,   # Capture errors
                text=True,                # Return error output as string
                check=True                # Raise exception if mysqldump fails
            )
        print(f"Exported to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to export to {output_file}")
        print("Error details:")
        print(e.stderr.strip())  # Show actual MySQL error message

def import_schema():
    """
    Export only the database schema (tables, structure, indexes),
    without any data.
    """
    args = [f"-u{DB_USER}", f"-p{DB_PASS}", "--no-data", DB_NAME]
    import_file(args, SCHEMA_FILE)

def import_data():
    """
    Export only the database data (INSERT statements),
    without table creation statements.
    """
    args = [f"-u{DB_USER}", f"-p{DB_PASS}", "--no-create-info", DB_NAME]
    import_file(args, DATA_FILE)

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    print("Starting database export...")
    import_schema()  # Export schema first
    import_data()    # Export data next
    print("Import script finished.")

