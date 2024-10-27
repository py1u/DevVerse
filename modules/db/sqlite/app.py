from flask import Flask,request
import json
import db 

DB = db.DatabaseDriver()

app = Flask("__name__")

def success_res(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_res(message, code=404):
    return json.dumps({"succes": False, "error": message}), code

@app.route("/tasks/")
def get_tasks():
    return sucess_res(DB.get_all_tasks())

@app.route("tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    description = body.get("description")
    task_id = DB.insert_task_table(description, False)
    task = DB.get_task_by_id(task_id)
    
    if task is not None:
        return success_res(task, 201)
    return failure_res("something went wrong while creating task!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
