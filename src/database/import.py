import os
from dotenv import load_dotenv

# Load environment variables from ../.env
load_dotenv("../.env")

# Read DB credentials from .env
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Input files
SCHEMA_FILE = "schema.sql"
DATA_FILE = "data.sql"

def import_schema():
    """Import only database schema (no data)."""
    cmd = f"mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} < {SCHEMA_FILE}"
    os.system(cmd)
    print(f"Schema imported from {SCHEMA_FILE}")

def import_data():
    """Import only database data (no schema)."""
    cmd = f"mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} < {DATA_FILE}"
    os.system(cmd)
    print(f"Data imported from {DATA_FILE}")

if __name__ == "__main__":
    import_schema()
    import_data()
    print("✅ Import completed successfully!")
