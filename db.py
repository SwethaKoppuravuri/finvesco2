import mysql.connector
from mysql.connector import Error

db_config = {
    'user': 'u880714964_sweetha',
    'password': 'Sweetha1@whitecolor',
    'host': '193.203.184.38',
    'database': 'u880714964_sweetha'
}

def create_connection():
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection