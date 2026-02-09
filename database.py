import cx_Oracle

# Database configuration
DB_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'dsn': 'localhost:1521/your_service_name'  # Format: hostname:port/service_name
}

def get_db_connection():
    """
    Creates and returns a connection to the Oracle database.
    """
    try:
        connection = cx_Oracle.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            dsn=DB_CONFIG['dsn']
        )
        return connection
    except cx_Oracle.Error as error:
        print(f"Database connection error: {error}")
        return None

def execute_query(query, params=None, fetchone=False, commit=False):
    """
    Executes a SQL query and returns the result.
    
    Args:
        query (str): The SQL query to execute
        params (dict/tuple): Parameters for the query
        fetchone (bool): Whether to fetch only one record
        commit (bool): Whether to commit after execution
        
    Returns:
        The query result or None on error
    """
    connection = get_db_connection()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if commit:
            connection.commit()
            
        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
            
        return result
    except cx_Oracle.Error as error:
        print(f"Database query error: {error}")
        return None
    finally:
        if connection:
            connection.close()
