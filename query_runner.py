from schema_reader import get_mysql_connection

def run_sql_query(query):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    headers = [i[0] for i in cursor.description]

    cursor.close()
    conn.close()

    return headers, rows
