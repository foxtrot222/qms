"""
Whitelist of allowed table names for SQL queries
This prevents SQL injection when using dynamic table names
"""

# Valid service queue table names
ALLOWED_QUEUE_TABLES = {
    'billing',
    'complaint',
    'kyc',
    'details transfer',
    'general enquiry',
    'identity verification',
    'meter related',
    'service disconnection',
    'ticket'
}

def validate_table_name(table_name):
    """
    Validates that a table name is in the allowed list
    Returns the table name if valid, raises ValueError otherwise
    """
    if not table_name:
        raise ValueError("Table name cannot be empty")
    
    # Normalize the table name
    normalized_name = str(table_name).lower().strip()
    
    if normalized_name not in ALLOWED_QUEUE_TABLES:
        raise ValueError(f"Invalid table name: {table_name}")
    
    return normalized_name

def sanitize_table_name(table_name):
    """
    Wraps table names with spaces in double quotes for SQLite
    """
    validated_name = validate_table_name(table_name)
    if ' ' in validated_name:
        return f'"{validated_name}"'
    return validated_name
