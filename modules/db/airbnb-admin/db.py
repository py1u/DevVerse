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
            
    def delete_booking_table(self):
        self.conn.execute("DROP TABLE IF EXISTS booking")
        print("booking table dropped!")
        
        
    def get_booking_table(self):
        cursor = self.conn.execute("SELECT * FROM booking;")
        print(cursor)
        bookings = []
        for row in cursor:
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            bookings.append(
                {
                    "name": row[0],
                    "address": row[1],
                    "rate": row[2],
                    "open": row[3]
                }
            )
        return bookings
    
    def get_booking_by_id():
        cursor = self.conn.execute("SELECT (name, address, rate, open) FROM booking WHERE id=?;", (id,))
        for row in cursor:
            return {"id": row[0], "description": row[1], "done": bool(row[2]) }
        return None
        
            
    