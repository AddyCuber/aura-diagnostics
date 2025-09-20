import sqlite3
import datetime

def log_step(diagnosis_id, message):
    """
    Logs a diagnostic step to the audit_log table in the audit.db database.
    
    Args:
        diagnosis_id (str): The ID of the diagnosis being performed
        message (str): The message to log
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('audit.db')
        cursor = conn.cursor()
        
        # Execute the INSERT statement
        cursor.execute(
            "INSERT INTO audit_log (diagnosis_id, message) VALUES (?, ?)",
            (diagnosis_id, message)
        )
        
        # Commit the transaction
        conn.commit()
        
    except Exception as e:
        print(f"Error logging to audit database: {e}")
        
    finally:
        # Close the connection
        if conn:
            conn.close()