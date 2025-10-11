import socket
import os

def get_available_port(start_port=5000, max_tries=10):
    """Find the next available port starting from start_port."""
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port  # Found an available port
            except OSError:
                port += 1  # Try next port
    raise OSError(f"No available port found from {start_port} to {port - 1}")
