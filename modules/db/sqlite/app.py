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
    return success_res(DB.get_all_tasks())

@app.route("/tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    description = body.get("description")
    task_id = DB.insert_task_table(description, 0)
    task = DB.get_task_by_id(task_id)
    
    if task is None:
        return failure_res("Task not found!")
    return success_res(task)

@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = DB.get_task_by_id(task_id)
    
    if not task:
        return failure_res("Task not found!")
    return success_res(task)

@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    task = DB.get_task_by_id(task_id)
    if not task:
        return failure_res("Task not found!")
    body = json.loads(request.data)
    description = body.


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = DB.get_task_by_id(task_id)
    if not task:
        return failure_res("Task not found!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


# Reference:

# def success_res(data, code=200):
#     return json.dumps({"success": True, "data": data}), code

# def failure_res(message, code=404):
#     return json.dumps({"succes": False, "error": message}), code

# @app.route("/tasks/")
# def get_tasks():
#     return success_res(DB.get_all_tasks())

# @app.route("/tasks/", methods=["POST"])
# def create_task():
#     body = json.loads(request.data)
#     description = body.get("description")
#     task_id = DB.insert_task_table(description, 0)
#     task = DB.get_task_by_id(task_id)
    
#     if task is None:
#         return failure_res("Task not found!")
#     return success_res(task)

# @app.route("/tasks/<int:task_id>/")
# def get_task(task_id):
#     task = DB.get_task_by_id(task_id)
#     if task is not None:
#         return success_res(task)
#     return failure_res("Task not found!")

# @app.route("/tasks/<int:task_id>/", methods=["POST"])
# def update_task(task_id):
#     body = json.loads(request.data)
#     description = body.get("description")
#     done = bool(body.get("done"))
#     DB.update_task_by_id(task_id, description, done)
    
#     task = DB.get_task_by_id(task_id)
#     if task is not None:
#         return success_res(task)
#     return failure_res("Task not found!")

# @app.route("/tasks/<int:task_id>/", methods=["DELETE"])
# def delete_task(task_id):
#     task = DB.get_task_by_id(task_id)
#     if task is not None:
#         DB.delete_task_by_id(task_id)
#         return success_res(task)
#     return failure_res("Task not found!")