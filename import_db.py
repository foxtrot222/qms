import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''),
    'database': os.getenv('DB_NAME', 'QMS'),
    'port': int(os.getenv('DB_PORT', 3306))
}

print(f"Connecting to MySQL at {config['host']}:{config['port']}...")
print(f"Database: {config['database']}, User: {config['user']}")

try:
    # Connect to MySQL server (without selecting database first)
    conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        port=config['port']
    )
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    print(f"\nCreating database '{config['database']}' if it doesn't exist...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
    cursor.execute(f"USE {config['database']}")
    print("✅ Database selected!")
    
    # Read and execute SQL file
    print("\nReading data.sql file...")
    with open('data.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Split by semicolon and execute each statement
    print("Executing SQL statements...")
    statements = sql_content.split(';')
    
    for i, statement in enumerate(statements):
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                cursor.execute(statement)
                if i % 10 == 0:
                    print(f"  Executed {i} statements...")
            except mysql.connector.Error as err:
                # Skip some common errors that don't matter
                if 'already exists' not in str(err) and 'Unknown database' not in str(err):
                    print(f"  Warning: {err}")
    
    conn.commit()
    print(f"\n✅ Successfully imported data.sql!")
    print(f"✅ Total statements executed: {len(statements)}")
    
    # Show tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📋 Tables in database '{config['database']}':")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Database import complete!")

except mysql.connector.Error as err:
    print(f"\n❌ MySQL Error: {err}")
    print("\nPlease check your database credentials in the .env file")
    exit(1)
except FileNotFoundError:
    print("\n❌ Error: data.sql file not found!")
    print("Make sure you're running this script from the qms directory")
    exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    exit(1)
