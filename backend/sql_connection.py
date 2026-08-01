import mysql.connector
import os

__cnx = None


def get_sql_connection():
    global __cnx

    if __cnx is None:
        print("Opening MySQL connection")

        __cnx = mysql.connector.connect(
            host="mysql-38021bf5-akritit009-ceb2.k.aivencloud.com",
            user="avnadmin",
            password="REMOVED",
            database="grocery_store",
            port=19567,
            ssl_ca=r"C:\Users\akrit\Downloads\ca.pem"
        )

        print("MySQL Connected Successfully")

    return __cnx