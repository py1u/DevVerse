import os
import sqlite3

def singleton(cls):
    instances = {}

    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    
    return getInstance

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
                    CREATE TABLE tasks
                    id INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0
                """
            )
            print("task table created!")
            
        except Exception as err:
            print(err)
                        
                        
    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT * FROM tasks;")
        tasks = []
        for row in cursor:
            tasks.append({
                "id": row[0],
                "description": row[1],
                "done": bool(row[2])
            })
        return tasks

        
DatabaseDriver = singleton(DatabaseDriver)  
            