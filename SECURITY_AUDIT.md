# QMS Project - Security Audit & Additional Bug Fixes

## Date: October 16, 2025 (Security Audit)

---

## CRITICAL SECURITY VULNERABILITIES FOUND

### 1. SQL Injection Vulnerabilities ⚠️ CRITICAL

**Issue:** Multiple routes use f-string formatting with user-controlled table names, creating SQL injection risks.

**Affected Files:**
- `src/routes/service_provider.py` (20+ instances)
- `src/routes/status.py` (2 instances)
- `src/routes/appointment.py` (5 instances)
- `src/routes/token.py` (1 instance)
- `src/routes/auth.py` (1 instance)
- `src/routes/admin.py` (1 instance)

**Vulnerable Code Pattern:**
```python
table_name = session.get('table_name')  # User-controlled
query = f"SELECT * FROM {table_name} WHERE..."  # SQL INJECTION!
cursor.execute(query)
```

**Attack Scenario:**
An attacker could manipulate the session to inject malicious SQL:
```python
table_name = "users; DROP TABLE token--"
# Results in: SELECT * FROM users; DROP TABLE token-- WHERE...
```

**Fix Applied:**
- Created `src/utils/security.py` with table name whitelist validation
- Added `sanitize_table_name()` function that:
  - Validates table names against allowed list
  - Prevents any table name not in the whitelist
  - Properly quotes table names with spaces
- Updated `service_provider.py` to use sanitized table names

**Status:** ✅ PARTIALLY FIXED (service_provider.py)
**Action Required:** Apply same fix to all other affected files

---

### 2. MySQL Syntax Still Present in SQLite Code

**Issue:** Despite converting to SQLite, many MySQL-specific syntax patterns remain.

**Problems Found:**

#### A. Parameter Placeholders
```python
# MySQL style (wrong for SQLite)
cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))

# SQLite style (correct)
cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
```

**Affected Files:** ALL route files
**Status:** ⚠️ NEEDS FIXING

#### B. Dictionary Cursor
```python
# MySQL style (wrong for SQLite)
cursor = conn.cursor(dictionary=True, buffered=True)

# SQLite style (correct - already set in db.py)
cursor = conn.cursor()
```

**Affected Files:**
- `appointment.py`
- `status.py`  
**Status:** ⚠️ NEEDS FIXING

#### C. Date/Time Functions
```python
# MySQL functions
TIME_FORMAT(time_slot, '%h:%i %p')
TIME_TO_SEC(log)
SEC_TO_TIME(avg_time)
NOW()

# SQLite equivalents needed
strftime('%H:%M', time_slot)
(strftime('%s', time) - strftime('%s', '00:00:00'))
time(seconds, 'unixepoch')
datetime('now')
```

**Affected Files:** ALL route files with time operations
**Status:** ⚠️ NEEDS FIXING

---

### 3. Missing Authentication on Sensitive Routes

**Issue:** Several routes don't check authentication, allowing unauthorized access.

**Vulnerable Routes:**

#### File: `routes/service_provider.py`
```python
@service_provider_bp.route("/get_queue")
def get_queue():
    table_name = session.get('table_name')  # Gets from session but no auth check!
```

**Missing Checks:**
- `/get_queue` - Should verify user_id in session
- `/get_dashboard_stats` - Should verify user_id in session
- `/complete_service` - Should verify user_id in session
- `/call_next` - Should verify user_id in session
- `/transfer_customer` - Should verify user_id in session

**Recommended Fix:**
```python
@service_provider_bp.route("/get_queue")
def get_queue():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    # ... rest of code
```

**Status:** ⚠️ NEEDS FIXING

---

### 4. Session Security Issues

**Issue:** Session data is trusted without validation.

**Problems:**

#### A. No Session Timeout
- Sessions never expire
- Logged-in users remain logged in forever
- **Fix:** Implement session timeout (e.g., 30 minutes)

#### B. No CSRF Protection
- All POST routes vulnerable to CSRF attacks
- **Fix:** Implement Flask-WTF CSRF protection or custom tokens

#### C. Weak Session Cookie Settings
```python
# Current (insecure)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# Recommended additions
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 min timeout
```

**Status:** ⚠️ NEEDS FIXING

---

### 5. Weak Password Storage (Admin Login)

**Issue:** Original code compared plain text passwords.

**Before:**
```python
if admin and (admin['password'] == adminPassword):
```

**After:**
```python
if admin and check_password_hash(admin['password'], adminPassword):
```

**Status:** ✅ FIXED

---

### 6. Missing Input Validation

**Issue:** User inputs are not validated before database operations.

**Examples:**

#### A. Email Validation
```python
# Current: No validation
email = request.form.get("emailAddress")

# Recommended: Validate format
import re
if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
    return jsonify({"success": False, "error": "Invalid email format"})
```

#### B. Integer Validation
```python
# Current: Direct conversion (can crash)
service_id = int(request.form.get("service"))

# Recommended: Safe conversion
try:
    service_id = int(request.form.get("service"))
except (ValueError, TypeError):
    return jsonify({"success": False, "error": "Invalid service ID"})
```

**Status:** ⚠️ NEEDS FIXING

---

### 7. Error Information Disclosure

**Issue:** Detailed error messages expose internal system information.

**Vulnerable Code:**
```python
except Exception as e:
    return jsonify({"success": False, "error": str(e)})
```

**Attack Use:** Attackers can trigger errors to learn about:
- Database structure
- File paths
- Internal logic

**Recommended Fix:**
```python
except Exception as e:
    logging.error(f"Error in function_name: {e}")  # Log detail
    return jsonify({"success": False, "error": "An internal error occurred"})  # Generic message
```

**Status:** ⚠️ NEEDS FIXING

---

### 8. Race Conditions in Queue Management

**Issue:** No locking mechanism for concurrent queue operations.

**Problem:**
Two users joining queue simultaneously could get same position.

```python
# User A and B execute this simultaneously
cursor.execute(f"SELECT MAX(position) FROM {table_name}")
max_pos = cursor.fetchone()['max_pos']  # Both get position 5
next_pos = max_pos + 1  # Both calculate position 6
cursor.execute(f"INSERT INTO {table_name} (position) VALUES (?)", (next_pos,))
# Both get position 6 - collision!
```

**Recommended Fix:**
- Use database transactions with proper isolation
- Implement row-level locking
- Use AUTO_INCREMENT for position or atomic operations

**Status:** ⚠️ NEEDS FIXING

---

### 9. Missing Rate Limiting

**Issue:** No protection against brute force attacks or DOS.

**Vulnerable Routes:**
- `/login` - Brute force password attempts
- `/adminlogin` - Brute force admin access
- `/request_otp` - OTP spam/DOS
- `/generate_token` - Token spam

**Recommended Fix:**
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    # ...
```

**Status:** ⚠️ NEEDS FIXING

---

### 10. Insecure OTP Implementation

**Issue:** OTP can be reused and has weak randomness.

**Problems:**

#### A. Predictable OTP
```python
def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))
```
- Uses `random` instead of `secrets` (cryptographically weak)

#### B. OTP Reuse
- OTPs not deleted after verification
- Same OTP can be used multiple times

**Recommended Fixes:**
```python
import secrets

def generate_otp(length=6):
    return ''.join(str(secrets.randbelow(10)) for _ in range(length))

# After verification:
cursor.execute("DELETE FROM otp_verification WHERE id = ?", (otp_id,))
```

**Status:** ⚠️ NEEDS FIXING

---

### 11. SendGrid API Key Exposure

**Issue:** API key visible in .env file (Git risk).

**Risk:** If .env is committed to Git, API key is exposed.

**Recommended Protection:**
1. Ensure `.env` is in `.gitignore`
2. Use environment variables on production server
3. Rotate API keys regularly
4. Use SendGrid's IP whitelisting

**Status:** ⚠️ REVIEW NEEDED

---

### 12. No HTTPS Enforcement

**Issue:** Application runs on HTTP by default.

**Risk:** 
- Passwords sent in clear text
- Session cookies can be intercepted
- Man-in-the-middle attacks

**Recommended Fix:**
```python
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

**Status:** ⚠️ NEEDS FIXING (Production)

---

## CODE QUALITY ISSUES

### 13. Inconsistent Error Handling

**Issue:** Mix of different error handling patterns.

**Examples:**
- Some functions return `None` on error
- Some raise exceptions
- Some return error tuples
- Some return JSON with success flags

**Recommendation:** Standardize on one pattern.

**Status:** ⚠️ IMPROVEMENT NEEDED

---

### 14. Missing Database Connection Cleanup

**Issue:** Some code paths don't close cursors/connections.

**Example:**
```python
cursor = conn.cursor()
if error_condition:
    return jsonify({"error": "..."})  # Connection not closed!
```

**Recommended Fix:** Use context managers:
```python
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        # ... code ...
```

**Status:** ⚠️ IMPROVEMENT NEEDED

---

### 15. Hardcoded Values

**Issue:** Magic numbers and strings throughout code.

**Examples:**
- OTP length: 6 (should be constant)
- OTP expiry: 5 minutes (should be config)
- Default factor: 0.5 (should be constant)
- Default service time: 180 seconds (should be config)

**Recommendation:** Create `config.py`:
```python
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
DEFAULT_VICINITY_KM = 0.5
DEFAULT_SERVICE_TIME_SECONDS = 180
```

**Status:** ⚠️ IMPROVEMENT NEEDED

---

## PRIORITY FIXES REQUIRED

### 🔴 CRITICAL (Fix Immediately)
1. ✅ SQL Injection vulnerabilities - PARTIALLY FIXED
2. ⚠️ MySQL syntax conversion to SQLite
3. ⚠️ Missing authentication checks
4. ✅ Weak password verification - FIXED

### 🟡 HIGH (Fix Before Production)
5. ⚠️ Session security configuration
6. ⚠️ Input validation
7. ⚠️ Error information disclosure
8. ⚠️ Rate limiting
9. ⚠️ Insecure OTP implementation
10. ⚠️ HTTPS enforcement

### 🟢 MEDIUM (Code Quality)
11. ⚠️ Inconsistent error handling
12. ⚠️ Database cleanup
13. ⚠️ Hardcoded values
14. ⚠️ Race conditions

---

## FIXES APPLIED IN THIS SESSION

### ✅ Completed

1. **Modal Not Opening** - Fixed JavaScript initialization
2. **Admin Direct Access** - Added authentication check
3. **Password Hashing** - Using `check_password_hash()`
4. **Table Name Validation** - Created whitelist system (partial)
5. **Database Migration** - Converted from MySQL to SQLite
6. **Close Function** - Uncommented modal close functionality

### 🔧 Partially Applied

1. **SQL Injection Protection** - Applied to `service_provider.py` only
   - **TODO:** Apply to all other affected files

### ⏳ Identified But Not Fixed

- All items marked ⚠️ above
- Require systematic refactoring
- Should be addressed before production deployment

---

## RECOMMENDED NEXT STEPS

1. **Immediate:** Complete SQL injection fixes for all files
2. **High Priority:** Fix MySQL→SQLite syntax conversion
3. **Security:** Add authentication decorators to all protected routes
4. **Code Quality:** Standardize error handling
5. **Configuration:** Move hardcoded values to config file
6. **Testing:** Add unit tests for security-critical functions
7. **Documentation:** Create security guidelines document

---

## FILES REQUIRING ADDITIONAL FIXES

- ⚠️ `src/routes/token.py` - MySQL syntax, SQL injection
- ⚠️ `src/routes/otp.py` - MySQL syntax, weak OTP, no rate limit
- ⚠️ `src/routes/status.py` - MySQL syntax, SQL injection
- ⚠️ `src/routes/appointment.py` - MySQL syntax, SQL injection
- ⚠️ `src/routes/service_provider.py` - MySQL syntax, auth checks
- ⚠️ `src/routes/admin.py` - MySQL syntax
- ⚠️ `src/routes/auth.py` - MySQL syntax
- ⚠️ `src/routes/check_in.py` - Input validation
- ⚠️ `src/routes/organization.py` - Session security

---

## SECURITY CHECKLIST FOR PRODUCTION

- [ ] All SQL injection vulnerabilities fixed
- [ ] All MySQL syntax converted to SQLite
- [ ] Authentication on all protected routes
- [ ] CSRF protection enabled
- [ ] Session timeout configured
- [ ] Secure cookie settings enabled
- [ ] Rate limiting implemented
- [ ] Input validation on all forms
- [ ] Error messages sanitized
- [ ] HTTPS enforced
- [ ] .env not in Git repository
- [ ] Strong SECRET_KEY generated
- [ ] API keys rotated and secured
- [ ] Database backups configured
- [ ] Logging configured (not console only)
- [ ] Security headers added (CSP, X-Frame-Options, etc.)

---

**⚠️ WARNING: This application should NOT be deployed to production until critical security issues are resolved.**
