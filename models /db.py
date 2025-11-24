import mysql.connector
from config import Config

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def execute_query(query, params=None, fetch=False, fetch_one=False):
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.lastrowid if cursor.lastrowid else True
        
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as err:
        print(f"Query execution error: {err}")
        if connection:
            connection.close()
        return None
