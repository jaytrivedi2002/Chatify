import sqlite3
from sqlite3 import Error
from datetime import datetime

# CONSTANTS

DATA_FILE = "data.db" #CHECK 
TABLE_OF_MESSAGES = "Messages"


class DataBase:
    def __init__(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect(DATA_FILE)
        except Error as e:
            print(e)

        self.cursor = self.connection.cursor()
        self.create_db_table()

    def close_connection(self):
        self.connection.close()

    def create_db_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE_OF_MESSAGES}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.connection.commit()

    def get_all_messages(self, limit=50, name=None):
        if not name:
            query = f"SELECT * FROM {TABLE_OF_MESSAGES}"
            self.cursor.execute(query)
        else:
            query = f"SELECT * FROM {TABLE_OF_MESSAGES} WHERE NAME = ?"
            self.cursor.execute(query, (name,))

        result = self.cursor.fetchall()

        # return messages in sorted order by date
        results = []
        for r in sorted(result, key=lambda x: x[3], reverse=True)[:limit]:
            name, content, date, _id = r
            data = {"name":name, "message":content, "time":str(date)}
            results.append(data)

        return list(reversed(results))

    def get_messages_by_name(self, name, limit=50):
        return self.get_all_messages(limit, name)

    def save_message(self, name, msg):
        query = f"INSERT INTO {TABLE_OF_MESSAGES} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, msg, datetime.now(), None))
        self.connection.commit()

