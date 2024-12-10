import os
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB")

    if not MYSQL_USER or not MYSQL_PASSWORD or not MYSQL_HOST or not MYSQL_DB:
        raise ValueError("Missing required database environment variables")

    return f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
