from flask import Flask
import json
import db 

DB = db.DatabaseDriver()

app = Flask("__name__")

def sucess_res(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_res(message, code=404):
    return json.dumps({"succes": False, "error": message}), code

@app.route("/tasks/")
def get_tasks():
    pass

@app.route("tasks/", methods=["POST"])
def create_task():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
