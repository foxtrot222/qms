import os

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
        
        # Replace conn.is_connected() with checking if conn is not None
        content = content.replace('if conn.is_connected():', 'if conn:')
        content = content.replace('if conn and conn.is_connected():', 'if conn:')
        content = content.replace('conn.is_connected()', 'conn is not None')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {os.path.basename(filepath)}")
    else:
        print(f"⚠️ File not found: {filepath}")

print("\n🎉 All files fixed!")
