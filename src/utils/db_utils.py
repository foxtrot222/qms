import re

def sanitize_service_name(service_name):
    # Replace non-alphanumeric characters with underscores
    return re.sub(r'[^a-zA-Z0-9_]', '_', service_name).lower()
