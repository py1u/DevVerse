import os
import sqlite3

def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class DatabaseDriver(object):

    def __init__(self):
        self.conn = sqlite3.connect(
            "booking.db", check_same_thread = False
        )
        self.create_booking_table()
        
    def create_booking_table(self):
        try:
            self.conn.execute(
            """
                CREATE TABLE booking (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    rate INTEGER NOT NULL,
                    open INTEGER DEFAULT 0
                )
            """
            )
            
        except Exception as err:
            print(err)
            
    