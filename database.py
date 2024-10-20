from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables from .env file
load_dotenv()
# Database setup
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER, 
        password=MYSQL_PASSWORD,  
        database=MYSQL_DATABASE
    )