# Queue Management System

A Project For Vikas Saptah Hackathon 2025

---

## Project Setup

### 1. Prerequisites

- **Python 3:** Make sure you have Python 3 installed on your system.
- **MySQL:** A running MySQL server instance is required.
- **pip:** Python's package installer, used to install project dependencies.

Install the required Python packages using pip:
```bash
pip install flask python-dotenv mysql-connector-python werkzeug sendgrid pyngrok
```

### 2. Database Setup

1.  **Create Database:** First, create a new database in your MySQL server that the application will use.
    ```sql
    CREATE DATABASE QMS;
    ```
2.  **Configure Environment:** Copy the `default.env` file to a new file named `.env` and fill in your database credentials (`DB_USER`, `DB_PASS`, `DB_NAME`).
3.  **Import Schema and Data:** Run the `export.py` script. This will set up all the necessary tables and import the initial data.
    ```bash
    python3 src/database/export.py
    ```
    *(Note: This script imports data into the database from the `.sql` files in `src/database/`.)*

### 3. Environment Variables

You must create a `.env` file in the root of the project with the following variables. You can copy `default.env` to get started. These variables are required for the application to run.

```
# Database credentials
DB_USER=
DB_PASS=
DB_NAME=

# Flask secret key for session management
SECRET_KEY=

# SendGrid API key for sending emails (token and OTP)
SENDGRID_API_KEY=
FROM_EMAIL=
FROM_NAME=

# Ngrok token for tunneling
NGROK_AUTHTOKEN=

# Port for the Flask application
PORT=
```

### 4. Running the Application

To run the application, you need to start the main server as a background process and then start the ngrok tunnel.

1.  **Start the Main Server (Background):**
    Open a terminal in the project root and run the main Flask application. The `&` at the end will run it as a background process.
    ```bash
    python3 src/main.py &
    ```

2.  **Start the Ngrok Tunnel:**
    In the same terminal, run the tunneling script. This will connect your local server to a public URL.
    ```bash
    python3 src/tunnel.py
    ```
    The script will output a public URL (e.g., `https://<random-string>.ngrok.io`). Use this URL to access the application in your browser.