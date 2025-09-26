import os
from dotenv import load_dotenv
from pyngrok import ngrok
import time

# Load environment variables from .env file
load_dotenv()

# Get the port and ngrok authtoken from environment variables
port = os.getenv('PORT', 5000)  # Default to 5000 if PORT is not set
ngrok_authtoken = os.getenv('NGROK_AUTHTOKEN')

# If the ngrok token is not set, raise an error
if not ngrok_authtoken:
    raise ValueError("NGROK_AUTHTOKEN is not set in the .env file.")

# Set the Ngrok authentication token
ngrok.set_auth_token(ngrok_authtoken)

# Establish the Ngrok tunnel
listener = ngrok.connect(port)

# Output the Ngrok URL to console
print(f"Ingress established at {listener.public_url}")

# Keep the listener alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing listener")
