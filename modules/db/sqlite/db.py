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

    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT * FROM task;")
        tasks = []
        for row in cursor:
            tasks.append(
                {
                    "id": row[0],
                    "description": row[1],
                    "done": bool(row[2])
                }
            )
        return tasks
    
    def insert_task_table(self, description, done):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO task (DESCRIPTION, DONE) VALUES (?,?);", (description, done)
            )
            self.conn.commit()
            return cur.lastrowid
        except Exception as err:
            print(err)
            return None

DatabaseDriver = singleton(DatabaseDriver)