import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Debug print to verify env variables are loaded correctly
print("🔍 Loaded Environment Variables:")
print("Host:", os.getenv("DB_HOST"))
print("Port:", os.getenv("DB_PORT"))
print("User:", os.getenv("DB_USER"))
print("Password:", os.getenv("DB_PASSWORD"))
print("Database:", os.getenv("DB_NAME"))
print()

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    if connection.is_connected():
        print("✅ Connected to MySQL successfully!\n")

        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        print("📋 Tables in the database:")
        for table in tables:
            print("-", table[0])

except Error as e:
    print("❌ Error connecting to MySQL:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("\n🔌 MySQL connection closed.")