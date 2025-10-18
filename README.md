> **⚠️ WARNING**
> 
> "**The working code for this project is available with the tag `v1.2`. Please note that most of the code was created with the assistance of large language models (LLMs). As such, this project is for demonstration and educational purposes only. **Do not use this application in a real-world environment where it could impact people or business operations.** The code may have limitations, security vulnerabilities, or other issues that make it unsuitable for production use.**"

# Queue Management System

A Project For Vikas Saptah Hackathon 2025

## Configuration

1.  Create a `.env` file in the root directory of the project.
2.  Copy the contents of `default.env` into the new `.env` file.
3.  Fill in the required environment variables in the `.env` file.

```
FLASK_ENV=development
SECRET_KEY=<Your Secret Key>
DB_HOST=<Your Database Host>
DB_USER=<Your Database User>
DB_PASS=<Your Database Password>
DB_NAME=<Your Database Name>
DB_PORT=<Your Database Port>
PORT=5000
SENDGRID_API_KEY=<Your Sendgrid API Key>
FROM_EMAIL=<Your From Email>
FROM_NAME=<Your From Name>
```

## Database Setup

1.  Make sure you have a MySQL server running.
2.  Create a new database with the name you specified in the `.env` file.
3.  Import the database schema and data from the `docs/data.sql` file using the following command:

    ```bash
    mysql -u <Your Database User> -p <Your Database Name> < docs/data.sql
    ```

## Running the Application

### Customer Side

To run the customer-facing application, execute the following command:

```bash
python3 src/app.py
```

The application will be available at `http://localhost:5000` by default, or on the port you specified in the `.env` file.

### Organization Side

To run the organization-facing application, execute the following command:

```bash
python3 src/orgapp.py
```

The application will run on the next available port after the one used by the customer-facing application. Check the console output to see the exact port number.

## Test Credentials

### Service Provider
- **Username:** SP001
- **Password:** password

### Admin
- **Username:** admin
- **Password:** password