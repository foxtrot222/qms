"""
Security fixes for SQL injection vulnerabilities and SQLite compatibility
This script fixes f-string SQL injections and MySQL-specific syntax
"""
import os
import re

files_to_fix = [
    r'd:\qmskb\qms\src\routes\token.py',
    r'd:\qmskb\qms\src\routes\otp.py',
    r'd:\qmskb\qms\src\routes\status.py',
    r'd:\qmskb\qms\src\routes\appointment.py',
    r'd:\qmskb\qms\src\routes\service_provider.py',
    r'd:\qmskb\qms\src\routes\admin.py',
    r'd:\qmskb\qms\src\routes\auth.py',
]

def fix_mysql_syntax(content):
    """Fix MySQL-specific syntax to SQLite"""
    # Replace %s with ? for parameter binding
    content = re.sub(r'VALUES\s*\(([^)]*%s[^)]*)\)', lambda m: 'VALUES (' + m.group(1).replace('%s', '?') + ')', content)
    content = re.sub(r'WHERE\s+([^=\s]+)\s*=\s*%s', r'WHERE \1 = ?', content)
    content = re.sub(r'AND\s+([^=\s]+)\s*=\s*%s', r'AND \1 = ?', content)
    
    # Replace cursor(dictionary=True, buffered=True) with cursor()
    content = content.replace('cursor(dictionary=True, buffered=True)', 'cursor()')
    content = content.replace('cursor(buffered=True, dictionary=True)', 'cursor()')
    content = content.replace('cursor(dictionary=True)', 'cursor()')
    
    # Replace TIME_FORMAT with strftime
    content = re.sub(
        r"TIME_FORMAT\(([^,]+),\s*'%h:%i\s*%p'\)",
        r"strftime('%H:%M', \1)",
        content
    )
    content = re.sub(
        r"TIME_FORMAT\(([^,]+),\s*'%H:%i:%S'\)",
        r"strftime('%H:%M:%S', \1)",
        content
    )
    content = re.sub(
        r"TIME_FORMAT\(SEC_TO_TIME\(AVG\(TIME_TO_SEC\(([^)]+)\)\)\),\s*'%i:%s'\)",
        r"AVG(\1)",
        content
    )
    
    # Replace NOW() with datetime('now')
    content = content.replace('NOW()', "datetime('now')")
    content = content.replace('expires_at > NOW()', "expires_at > datetime('now')")
    
    # Replace TIME_TO_SEC with custom handling
    content = re.sub(
        r'TIME_TO_SEC\(([^)]+)\)',
        r"(strftime('%s', \1) - strftime('%s', '00:00:00'))",
        content
    )
    
    # Replace SEC_TO_TIME with time()
    content = re.sub(
        r'SEC_TO_TIME\(([^)]+)\)',
        r'time(\1, "unixepoch")',
        content
    )
    
    return content

for filepath in files_to_fix:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_mysql_syntax(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed MySQL syntax in {os.path.basename(filepath)}")
        else:
            print(f"⏭️ No changes needed in {os.path.basename(filepath)}")

print("\n🎉 MySQL syntax fixes complete!")
