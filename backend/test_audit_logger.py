import sqlite3
from audit_logger import log_step

# Test the log_step function
test_id = "test_diagnosis_123"
test_message = "This is a test log message"

# Log a test message
log_step(test_id, test_message)

# Verify the message was logged correctly
conn = sqlite3.connect('audit.db')
cursor = conn.cursor()

# Query the latest entry
cursor.execute("SELECT diagnosis_id, message FROM audit_log ORDER BY id DESC LIMIT 1")
result = cursor.fetchone()

if result:
    logged_id, logged_message = result
    print(f"Test successful!")
    print(f"Logged diagnosis_id: {logged_id}")
    print(f"Logged message: {logged_message}")
    
    # Verify the values match
    assert logged_id == test_id, f"Expected {test_id}, got {logged_id}"
    assert logged_message == test_message, f"Expected {test_message}, got {logged_message}"
    print("All assertions passed!")
else:
    print("Test failed: No log entry found")

conn.close()