import mysql.connector
import os
from dotenv import load_dotenv

from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

__cnx = None

def get_sql_connection():
    global __cnx

    if __cnx is None:
        print("Opening MySQL connection")

        print("HOST:", os.getenv("DB_HOST"))
        print("USER:", os.getenv("DB_USER"))
        print("DB:", os.getenv("DB_NAME"))
        print("PORT:", os.getenv("DB_PORT"))

        __cnx = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")),
            ssl_ca=os.getenv("SSL_CA")
        )

        print("MySQL Connected Successfully")

    return __cnx