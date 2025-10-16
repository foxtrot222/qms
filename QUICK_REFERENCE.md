# QMS Project - Quick Reference

## 🚀 Quick Start

```powershell
cd d:\qmskb\qms\src
python orgapp.py
```

Visit: http://localhost:5001

---

## 🔑 Default Credentials

**Admin:** `admin` / `admin123`  
**Officer:** `officer1` / `password123`

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `qms.db` | SQLite database |
| `.env` | Configuration (don't commit!) |
| `BUG_FIXES.md` | Bugs fixed today |
| `SECURITY_AUDIT.md` | Security issues found |
| `SUMMARY.md` | Complete overview |

---

## ✅ What Works

- ✅ Login modals open correctly
- ✅ Admin authentication required
- ✅ SQLite database (no password needed)
- ✅ Password hashing

---

## ⚠️ What Needs Fixing

- ⚠️ SQL injection in 25+ places
- ⚠️ MySQL syntax still present
- ⚠️ Missing auth on most routes
- ⚠️ No rate limiting
- ⚠️ Weak OTP implementation

**See `SECURITY_AUDIT.md` for details**

---

## 🛠️ How to Apply Fixes

### Add Authentication to Route:
```python
from utils.decorators import login_required

@app.route('/protected')
@login_required  # Add this decorator
def protected_route():
    # ...
```

### Fix SQL Injection:
```python
from utils.security import sanitize_table_name

# Before (vulnerable):
cursor.execute(f"SELECT * FROM {table_name}")

# After (safe):
safe_table = sanitize_table_name(table_name)
cursor.execute(f"SELECT * FROM {safe_table}")
```

### Fix MySQL Syntax:
```python
# Before (MySQL):
cursor.execute("SELECT * FROM user WHERE id = %s", (id,))

# After (SQLite):
cursor.execute("SELECT * FROM user WHERE id = ?", (id,))
```

---

## 📊 Project Stats

- **Files Modified:** 15+
- **Bugs Fixed:** 6
- **Security Issues Found:** 15
- **Documentation Created:** 4 files
- **Database:** SQLite (qms.db)
- **Status:** Development Only

---

## ⚠️ Production Checklist

Before deploying to production:

- [ ] Fix all SQL injection issues
- [ ] Convert all MySQL syntax
- [ ] Add authentication to all routes
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Configure session security
- [ ] Enable HTTPS
- [ ] Change default passwords
- [ ] Remove debug mode
- [ ] Add logging

---

## 📞 Help

- **Bugs Fixed:** See `BUG_FIXES.md`
- **Security Issues:** See `SECURITY_AUDIT.md`  
- **Full Overview:** See `SUMMARY.md`
- **Original Docs:** See `README.md`
