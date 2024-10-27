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
            "task.db", check_same_thread = False
        )
        self.create_task_table()
        
    def create_task_table(self):
        try:
            self.conn.execute(
            """
                CREATE TABLE task (
                    ID INTEGER PRIMARY KEY,
                    DESCRIPTION TEXT NOT NULL,
                    DONE INTEGER NOT NULL        
                );
            """
            )
        except Exception as err:
            print(err)
    
    def delete_task_table(self):
        self.conn.execute("DROP TABLE IF EXISTS task;")

    

DatabaseDriver = singleton(DatabaseDriver)