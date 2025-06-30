# db.py

import mysql.connector
from mysql.connector import Error
import sys

class Database:
    def __init__(self, host="localhost", user="root", password="", database="task_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            print(f"[DB ERROR] {e}")
            sys.exit(1)

    def execute(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            if not query.strip().lower().startswith("select"):
                self.conn.commit()
            return True
        except Error as e:
            print(f"[EXEC ERROR] {e}") 
            return False


    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
