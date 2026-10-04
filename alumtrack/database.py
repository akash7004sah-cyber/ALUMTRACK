import sqlite3

DATABASE = "alumtrack.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def get_all_alumni():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM alumni")

    data = cursor.fetchall()

    connection.close()

    return data