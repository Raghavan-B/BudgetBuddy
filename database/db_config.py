import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_CONFIG = {
    "host":os.getenv("DB_HOST"),
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
    "database":os.getenv("DB_DATABASE"),
}

def get_connection():
    conn =  mysql.connector.connect(**DB_CONFIG)
    return conn

def close_connection(conn):
    conn.close()

