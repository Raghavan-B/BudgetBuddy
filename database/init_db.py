import mysql.connector
from db_config import DB_CONFIG

def initialize_database():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    with open("create_tables.sql","r") as sql_file:
        sql_script = sql_file.read()
    cursor.execute(sql_script,multi=True)
    print("Database Initialized Successfully")
    
    # connection.commit()
    # cursor.close()
    # connection.close()
    

if __name__ == "__main__":
    initialize_database() 