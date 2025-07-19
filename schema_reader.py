import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def read_schema():
    conn = get_mysql_connection()
    cursor = conn.cursor()

    query = """
    SELECT table_name, column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema = %s 
    ORDER BY table_name, ordinal_position
    """
    cursor.execute(query, (os.getenv("DB_NAME"),))
    results = cursor.fetchall()

    schema = {}
    for table_name, column_name, data_type in results:
        if table_name not in schema:
            schema[table_name] = []
        schema[table_name].append(f"{column_name} ({data_type})")

    cursor.close()
    conn.close()
    return schema
