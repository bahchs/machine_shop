import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Bach2308_.',
        database='machine_shop'
    )
    return connection