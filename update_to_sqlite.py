import os
import re

# Files to update
files = [
    r'd:\qmskb\qms\src\routes\token.py',
    r'd:\qmskb\qms\src\routes\organization.py',
    r'd:\qmskb\qms\src\routes\auth.py',
    r'd:\qmskb\qms\src\routes\admin.py',
    r'd:\qmskb\qms\src\routes\status.py',
    r'd:\qmskb\qms\src\routes\appointment.py',
    r'd:\qmskb\qms\src\routes\check_in.py',
    r'd:\qmskb\qms\src\routes\otp.py',
    r'd:\qmskb\qms\src\routes\service_provider.py',
]

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace mysql.connector with sqlite3
        content = content.replace('mysql.connector.Error', 'sqlite3.Error')
        content = content.replace('import mysql.connector', 'import sqlite3')
        
        # Replace cursor(dictionary=True) with regular cursor
        # SQLite rows already work like dicts with row_factory set
        content = content.replace('cursor(dictionary=True)', 'cursor()')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {os.path.basename(filepath)}")
    else:
        print(f"⚠️ File not found: {filepath}")

print("\n🎉 All files updated!")
