import sqlite3

def parse_row(row, columns):
    parsed_row = {}
    for item in range(len(columns)):
        parsed_row[columns[item]] = row[item]
    return parsed_row

def parse_cursor(cursor, columns):
    return [parse_row(row, columns) for row in cursor]

def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
 
    def __init__(self):
        self.conn = sqlite3.connect("task.db", check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.create_task_table()
        self.create_subtask_table()
        
    def create_task_table(self):

        try:
            self.conn.execute(
                """
                CREATE TABLE tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    done INTEGER NOT NULL
                );
            """
            )
        except Exception as err:
            print(err)

    def delete_task_table(self):
        self.conn.execute("DROP TABLE IF EXISTS tasks;")

    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT * FROM tasks;")
        tasks = parse_cursor(cursor, ["id", "description", "done"])        
        return tasks

    def insert_task_table(self, description, done):
        cursor = self.conn.execute("INSERT INTO tasks (description, done) VALUES (?, ?);", (description, done))
        self.conn.commit()
        return cursor.lastrowid

    def get_task_by_id(self, id):
        cursor = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        for row in cursor:
            return parse_row(row, ["id", "description", "done"])
        return None

    def update_task_by_id(self, id, description, done):
        self.conn.execute(
            """
            UPDATE tasks
            SET description = ?, done = ?
            WHERE id = ?;
            """,
            (description, done, id),
        )
        self.conn.commit()

    def delete_task_by_id(self, id):
        
        self.conn.execute(
            """
            DELETE FROM tasks
            WHERE id = ?;
            """,
            (id,),
        )
        self.conn.commit()

    def create_subtask_table(self):
        try:
            self.conn.execute(
                """
                    CREATE TABLE subtask (
                        id INTEGER PRIMARY KEY,
                        description TEXT NOT NULL,
                        done INTEGER NOT NULL,
                        task_id INTEGER NOT NULL,
                        FOREIGN KEY (task_id) REFERENCES tasks(id)
                    );
                """
            )
            
        except Exception as err:
            print(err)
        
DatabaseDriver = singleton(DatabaseDriver)