> **⚠️ WARNING**
>
> "**The working code for this project is available with the tag `v1.1`. Please note that most of the code was created with the assistance of large language models (LLMs). As such, this project is for demonstration and educational purposes only. **Do not use this application in a real-world environment where it could impact people or business operations.** The code may have limitations, security vulnerabilities, or other issues that make it unsuitable for production use.**"

# Queue Management System

A Project For Vikas Saptah Hackathon 2025

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Default Credentials](#default-credentials)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

### 1. Python 3.8 or higher
Check if Python is installed:
```bash
python --version
# or
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### 2. SQLite3
SQLite3 usually comes pre-installed with Python. Verify installation:
```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

**Windows Installation (if needed):**
- SQLite is bundled with Python, no separate installation required
- Alternatively, download from [sqlite.org/download.html](https://www.sqlite.org/download.html)

**Linux Installation (if needed):**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install sqlite3

# Fedora/RHEL
sudo dnf install sqlite

# Arch Linux
sudo pacman -S sqlite
```

**macOS Installation (if needed):**
```bash
# Using Homebrew
brew install sqlite3
```

### 3. Git (Optional, for cloning the repository)
```bash
git --version
```

## 📦 Installation

### Step 1: Clone or Download the Project
```bash
# If using Git
git clone <repository-url>
cd qms

# Or download and extract the ZIP file, then navigate to the folder
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Linux/macOS
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
# Make sure you're in the qms directory and virtual environment is activated
pip install -r src/requirements.txt
```

**Required packages include:**
- Flask==2.3.3
- python-dotenv
- sendgrid
- Werkzeug

## 🗄️ Database Setup

This project uses **SQLite** (a file-based database) - no separate database server installation required!

### Option 1: Use Pre-configured Database (Recommended)
The project comes with a pre-configured SQLite database (`qms.db`) with test data:

```bash
# Verify the database exists
# Windows (PowerShell)
Test-Path "qms.db"

# Linux/macOS
ls -l qms.db
```

If the file exists, you're ready to go! Skip to [Configuration](#configuration).

### Option 2: Initialize Fresh Database
If you need to create a fresh database:

```bash
# Navigate to the project root directory
cd qms

# Run the initialization script
python init_sqlite_db.py
```

This will:
- Create a new `qms.db` file
- Set up all necessary tables (users, organizations, tokens, appointments, etc.)
- Insert sample data for testing

**Sample Data Includes:**
- 1 Admin user
- 2 Service providers (officers)
- 1 Organization
- Sample queues and appointments

## ⚙️ Configuration

### Step 1: Create Environment File
```bash
# Copy the default environment file
# Windows (PowerShell)
Copy-Item default.env .env

# Linux/macOS
cp default.env .env
```

### Step 2: Edit `.env` File
Open the `.env` file in a text editor and configure:

```env
# Application Settings
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
PORT=5000

# SendGrid Email Configuration (for OTP and notifications)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=your-verified-sender@example.com
FROM_NAME=QMS System

# Database Configuration (SQLite - no changes needed)
# The database file is located at: qms.db
```

**Important Notes:**
- **SECRET_KEY**: Generate a strong random key for production
- **SENDGRID_API_KEY**: Get a free API key from [SendGrid](https://sendgrid.com/)
- **FROM_EMAIL**: Must be verified in your SendGrid account
- Database settings (DB_HOST, DB_USER, etc.) are **NOT needed** for SQLite

### Step 3: Generate Secret Key (Production)
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and use it as your `SECRET_KEY` in `.env`

## 🚀 Running the Application

The QMS has two separate applications:

### 1. Customer-Facing Application (Port 5000)
For customers to book appointments and check status:

```bash
# Navigate to src directory
cd src

# Run the customer app
python app.py
```

Access at: **http://localhost:5000**

### 2. Organization-Facing Application (Port 5001)
For service providers and admins:

```bash
# Navigate to src directory (if not already there)
cd src

# Run the organization app
python orgapp.py
```

Access at: **http://localhost:5001**

### Running Both Applications

**Option 1: Two Terminal Windows**
- Terminal 1: `python src/app.py`
- Terminal 2: `python src/orgapp.py`

**Option 2: Background Process (Linux/macOS)**
```bash
python src/app.py &
python src/orgapp.py &
```

**Option 3: Using Screen/Tmux (Linux/macOS)**
```bash
# Using screen
screen -S customer-app
python src/app.py
# Press Ctrl+A, then D to detach

screen -S org-app
python src/orgapp.py
# Press Ctrl+A, then D to detach
```

### Stopping the Application
- Press `Ctrl+C` in the terminal where the app is running
- Or kill the process:
  ```bash
  # Windows (PowerShell)
  Get-Process python | Stop-Process
  
  # Linux/macOS
  pkill -f "python.*app.py"
  ```

## 🔑 Default Credentials

### Admin Panel Access
- **Username:** `admin`
- **Password:** `admin123`
- **Access URL:** http://localhost:5001 → Click "Admin Login"

### Service Provider Dashboard
- **Username:** `officer1`
- **Password:** `password123`
- **Access URL:** http://localhost:5001 → Click "Access Dashboard"

**⚠️ IMPORTANT:** Change these default passwords before deploying to production!

## 📁 Project Structure

```
qms/
├── qms.db                      # SQLite database file
├── .env                        # Environment configuration (create from default.env)
├── default.env                 # Template for environment variables
├── schema.sql                  # MySQL schema (legacy)
├── schema_sqlite.sql           # SQLite schema
├── init_sqlite_db.py          # Database initialization script
├── README.md                   # This file
├── BUG_FIXES.md               # Bug fixes documentation
├── SECURITY_AUDIT.md          # Security issues and recommendations
├── SUMMARY.md                 # Complete project overview
├── QUICK_REFERENCE.md         # Quick start guide
└── src/
    ├── app.py                 # Customer-facing application
    ├── orgapp.py              # Organization-facing application
    ├── requirements.txt       # Python dependencies
    ├── models/
    │   ├── __init__.py
    │   └── db.py              # Database connection handler (SQLite)
    ├── routes/
    │   ├── __init__.py
    │   ├── admin.py           # Admin panel routes
    │   ├── appointment.py     # Appointment management
    │   ├── auth.py            # Authentication
    │   ├── check_in.py        # Check-in functionality
    │   ├── main.py            # Main routes
    │   ├── organization.py    # Organization management
    │   ├── otp.py             # OTP generation and verification
    │   ├── service_provider.py # Service provider dashboard
    │   ├── status.py          # Token status checking
    │   └── token.py           # Token generation
    ├── static/
    │   ├── style.css
    │   ├── officemap.png
    │   └── js/               # JavaScript modules
    ├── templates/            # HTML templates
    └── utils/
        ├── __init__.py
        ├── email_utils.py    # Email sending utilities
        ├── security.py       # Security utilities
        └── decorators.py     # Authentication decorators
```

## 🔍 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install dependencies
```bash
pip install -r src/requirements.txt
```

### Issue: "Database is locked"
**Solution:** Close any other programs accessing `qms.db` or delete `qms.db-journal` file
```bash
# Windows
Remove-Item qms.db-journal -ErrorAction SilentlyContinue

# Linux/macOS
rm -f qms.db-journal
```

### Issue: "Port already in use"
**Solution:** Change the port in `.env` file or kill the process using the port
```bash
# Windows - Find process on port 5000
netstat -ano | findstr :5000
# Then kill it with: taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:5000 | xargs kill -9
```

### Issue: "Template not found"
**Solution:** Make sure you're running the app from the `src` directory
```bash
cd src
python app.py
```

### Issue: Email/OTP not sending
**Solution:** 
1. Verify SendGrid API key in `.env`
2. Verify sender email is verified in SendGrid
3. Check SendGrid dashboard for error logs

### Issue: Can't login with default credentials
**Solution:** Reinitialize the database
```bash
# Backup current database if needed
Copy-Item qms.db qms.db.backup

# Reinitialize
python init_sqlite_db.py
```

## 📚 Additional Documentation

- **BUG_FIXES.md** - List of all bugs fixed during development
- **SECURITY_AUDIT.md** - Security vulnerabilities and recommendations
- **SUMMARY.md** - Detailed project overview and changes
- **QUICK_REFERENCE.md** - Quick start guide and important notes

## 🛡️ Security Notice

**This application is for demonstration and educational purposes only.**

Before deploying to production:
1. Change all default passwords
2. Review `SECURITY_AUDIT.md` for known vulnerabilities
3. Use a production-grade WSGI server (not Flask development server)
4. Enable HTTPS
5. Implement rate limiting
6. Review and implement security recommendations

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

This is a hackathon project. For major changes, please open an issue first to discuss what you would like to change.

---

**For quick start:** See `QUICK_REFERENCE.md`  
**For complete project details:** See `SUMMARY.md`
