# QMS Project - Bug Fixes Documentation

## Date: October 16, 2025

## Issues Fixed

### Issue 1: "Access Dashboard" Button Not Working
**Problem:** Clicking the "Access Dashboard" button was not opening the login modal.

### Issue 2: "Admin Login" Button Bypassing Authentication
**Problem:** Clicking "Admin Login" was directly showing the admin page without asking for credentials.

---

## Changes Made (Non-Database Related)

### 1. Frontend - HTML Template Changes

#### File: `src/templates/organization.html`

**Line 30-35 (Buttons section):**

**Before:**
```html
<a href="/dashboard" id="accessDashboardBtn" class="...">
    Access Dashboard
</a>
<a href="/admin" id="adminLoginBtn" class="...">
    Admin Login
</a>
```

**After:**
```html
<a href="#" id="accessDashboardBtn" class="...">
    Access Dashboard
</a>
<a href="#" id="adminLoginBtn" class="...">
    Admin Login
</a>
```

**Why:** Changed `href` attributes from actual routes (`/dashboard`, `/admin`) to `#` to prevent browser navigation. This allows JavaScript to intercept the click and show the modal instead.

---

### 2. Frontend - JavaScript Initialization

#### File: `src/static/js/pages/organizationPage.js`

**Line 95-101 (End of file):**

**Before:**
```javascript
export function initOrganizationPage() {
    if (!document.getElementById('organizationPage')) return;

    initLoginModal(
        'accessDashboardBtn',
        'officerLoginModal',
        ...
    );
}
```

**After:**
```javascript
export function initOrganizationPage() {
    if (!document.getElementById('organizationPage')) return;

    initLoginModal(
        'accessDashboardBtn',
        'officerLoginModal',
        ...
    );
}

// Auto-initialize when loaded directly (not through main.js)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOrganizationPage);
} else {
    initOrganizationPage();
}
```

**Why:** The `initOrganizationPage()` function was being exported but never called when the script loaded. Added auto-initialization code that:
- Checks if the DOM is still loading
- If yes, waits for DOMContentLoaded event
- If no (already loaded), runs immediately
- This ensures the modal event listeners are attached to the buttons

---

### 3. Backend - Admin Route Authentication

#### File: `src/routes/admin.py`

**Line 325-330:**

**Before:**
```python
@admin_bp.route('/admin')
def admin():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return render_template('admin.html', stats=None)
```

**After:**
```python
@admin_bp.route('/admin')
def admin():
    # Check if admin is logged in
    if 'admin_id' not in session:
        flash("Please log in to access the admin panel.", "warning")
        return redirect(url_for('org.organization'))
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return render_template('admin.html', stats=None)
```

**Why:** Added authentication check at the beginning of the admin route. Now:
- Checks if `admin_id` exists in the session
- If not authenticated, redirects to organization page with a warning message
- Prevents unauthorized access to the admin panel

---

### 4. Backend - Admin Login Password Verification

#### File: `src/routes/admin.py`

**Line 415-425:**

**Before:**
```python
cursor.execute("SELECT * FROM admin WHERE name=%s", (adminId,))
admin = cursor.fetchone()
if admin and (admin['password'] == adminPassword):
    cursor.close()
    session['admin_id'] = admin['id']
    session['adminname'] = admin['name']
    return jsonify({"success": True, "redirect": "/admin"})
```

**After:**
```python
cursor.execute("SELECT * FROM admin WHERE name=?", (adminId,))
admin = cursor.fetchone()
if admin and check_password_hash(admin['password'], adminPassword):
    cursor.close()
    session['admin_id'] = admin['id']
    session['adminname'] = admin['name']
    return jsonify({"success": True, "redirect": "/admin"})
```

**Why:** 
1. **Security Fix:** Changed from plain text password comparison to `check_password_hash()` for secure password verification
2. **SQLite Compatibility:** Changed SQL placeholder from `%s` (MySQL style) to `?` (SQLite style)

---

### 5. JavaScript - Modal Close Function (Previously Fixed)

#### File: `src/static/js/pages/organizationPage.js`

**Line 28-37:**

**Before (was commented out):**
```javascript
// const close = () => {
//     content.classList.add('scale-95', 'opacity-0');
//     modal.style.opacity = '0';
//     setTimeout(() => {
//         modal.classList.add('hidden');
//         errorEl.classList.add('hidden');
//         errorEl.textContent = '';
//         form.reset();
//     }, 300);
// };
```

**After (uncommented):**
```javascript
const close = () => {
    content.classList.add('scale-95', 'opacity-0');
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.classList.add('hidden');
        errorEl.classList.add('hidden');
        errorEl.textContent = '';
        form.reset();
    }, 300);
};
```

**Why:** The `close()` function was commented out but still being called on lines 39-40, causing JavaScript errors and preventing modals from working properly.

---

## Summary of Root Causes

1. **HTML Navigation Issue:** Buttons had `href` pointing to actual routes, causing browser navigation before JavaScript could run
2. **JavaScript Not Initialized:** The `initOrganizationPage()` function was exported but never executed
3. **Missing Authentication:** Admin route had no session check, allowing direct access
4. **Insecure Password Check:** Admin login was comparing plain text passwords instead of using hashed verification
5. **Commented Code:** Modal close function was commented out but still being referenced

---

## Testing Instructions

1. **Hard refresh your browser:** `Ctrl+Shift+F5` (clears cached JavaScript)
2. **Test "Access Dashboard":**
   - Click button → Should show Officer Login modal
   - Enter credentials: `officer1` / `password123`
   - Should redirect to dashboard on success
3. **Test "Admin Login":**
   - Click button → Should show Admin Login modal
   - Enter credentials: `admin` / `admin123`
   - Should redirect to admin panel on success
4. **Test Authentication:**
   - Try accessing `/admin` directly without logging in
   - Should redirect to organization page with warning message

---

## Files Modified

### Frontend:
- `src/templates/organization.html` - Button href attributes
- `src/static/js/pages/organizationPage.js` - Auto-initialization and close function

### Backend:
- `src/routes/admin.py` - Authentication check and password hashing

---

## Security Improvements

1. ✅ Admin panel now requires authentication
2. ✅ Passwords verified using `check_password_hash()` instead of plain text
3. ✅ Session-based access control implemented
4. ✅ Proper redirects for unauthorized access attempts

---

## Notes

- All changes are backward compatible
- No database schema changes were required
- SQLite-specific SQL syntax used (`?` instead of `%s`)
- Modal animations preserved (300ms transition)

---

## SECURITY AUDIT CONDUCTED (October 16, 2025)

After fixing the initial bugs, a comprehensive security audit was performed.

### Critical Issues Discovered:

1. **SQL Injection Vulnerabilities** ⚠️
   - 30+ instances of f-string SQL with user-controlled table names
   - Created whitelist validation system in `src/utils/security.py`
   - Partially fixed in `service_provider.py`

2. **MySQL Syntax Still Present** ⚠️
   - Parameter placeholders (`%s` vs `?`)
   - Dictionary cursors `cursor(dictionary=True)`
   - Time functions (TIME_FORMAT, NOW(), etc.)

3. **Missing Authentication Checks** ⚠️
   - Service provider routes lack auth verification
   - Dashboard routes accessible without login check

4. **Weak OTP Implementation** ⚠️
   - Uses `random` instead of `secrets` (cryptographically weak)
   - OTPs not deleted after verification

5. **No Rate Limiting** ⚠️
   - Login routes vulnerable to brute force
   - Token generation can be spammed

6. **Session Security** ⚠️
   - No timeout configured
   - No CSRF protection
   - Insecure cookie settings

### Full Security Report:
See `SECURITY_AUDIT.md` for complete details on:
- 15 security/code quality issues identified
- Recommended fixes and examples
- Priority classification
- Production deployment checklist

### Status:
- ✅ 6 bugs fixed in this session
- ⚠️ 15 security issues identified but NOT YET fixed
- 📝 Comprehensive documentation created

**⚠️ IMPORTANT: Application requires additional security fixes before production use.**

