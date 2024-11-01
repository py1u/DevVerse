from flask import Flask, request
import json

app = Flask("__main__")

tasks = {
    0:{
        "id": 0,
        "description": "learn backend",
        "done": False,
    },
    1:{
        "id": 1,
        "description": "eat apple pie",
        "done": False
    }   
}


task_id_counter = 2

@app.route("/")
def home():
    return "Hello World!"

@app.route("/tasks/")
def get_tasks():
    data = list(tasks.values())
    response = {
        "success": True,
        "data": data
    }
    return json.dumps(response), 200

@app.route("/tasks/", methods=["POST"])
def create_task():
    global task_id_counter
    body = json.loads(request.data)
    description = body.get("description")
    task = {
        "id": task_id_counter,
        "desciption": description,
        "done": False
    }
    tasks[task_id_counter] = task
    task_id_counter += 1
    return json.dumps({"success": True, "data": task}), 201
    
@app.route("/tasks/<int:task_id>/")
def get_task_by_id(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"success": False, "error": "task not found!"}), 404
    return json.dumps({"success": True, "data": task}), 200    
    
@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task_by_id(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"success": False, "error": "task not found"}), 404
    body = json.loads(request.data)
    description = body.get("description")
    done = body.get("done")
    task["description"] = description
    task["done"] = done
    return json.dumps({"success": True, "data": task}), 200

@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"success": False, "error": "task not found!"}), 404
    del tasks[task_id]
    return json.dumps({"success": True, "data": task}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    
    