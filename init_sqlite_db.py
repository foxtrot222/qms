import sqlite3
import os
from werkzeug.security import generate_password_hash

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'qms.db')

print(f"Creating SQLite database at: {DB_PATH}")

# Remove old database if exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("✅ Removed old database")

# Create new database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("📦 Creating tables...")

# Read and execute schema
with open('schema_sqlite.sql', 'r', encoding='utf-8') as f:
    schema = f.read()
    cursor.executescript(schema)

print("✅ Tables created successfully!")

# Add default admin with proper password hash
admin_password = generate_password_hash('admin123')
cursor.execute("""
    INSERT OR REPLACE INTO admin (id, name, password, factor, latitude, longitude) 
    VALUES (1, 'admin', ?, 1.0, 0.0, 0.0)
""", (admin_password,))

# Add default services
services = [
    (1, 'billing'),
    (2, 'complaint'),
    (3, 'kyc'),
    (4, 'general enquiry'),
    (5, 'identity verification'),
    (6, 'meter related'),
    (7, 'service disconnection'),
    (8, 'details transfer')
]

for service_id, service_name in services:
    cursor.execute("INSERT OR REPLACE INTO service (id, name) VALUES (?, ?)", (service_id, service_name))

print("✅ Added default services")

# Add default service provider
officer_password = generate_password_hash('password123')
cursor.execute("""
    INSERT OR REPLACE INTO service_provider (id, name, service_id, officerID, password) 
    VALUES (1, 'Test Officer', 1, 'officer1', ?)
""", (officer_password,))

print("✅ Added default service provider")

# Add some sample appointment slots
import datetime
start_time = datetime.time(9, 0)  # 9:00 AM
for i in range(20):  # 20 slots from 9 AM to 6 PM
    hour = 9 + (i // 2)
    minute = 30 if i % 2 else 0
    time_slot = f"{hour:02d}:{minute:02d}:00"
    cursor.execute("INSERT INTO appointment (time_slot, is_booked) VALUES (?, 0)", (time_slot,))

print("✅ Added appointment slots")

conn.commit()
conn.close()

print("\n🎉 Database initialized successfully!")
print(f"📍 Database location: {DB_PATH}")
print("\n📝 Default credentials:")
print("   Admin: username='admin', password='admin123'")
print("   Officer: officerID='officer1', password='password123'")
