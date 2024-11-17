from flask import Flask, request
import json
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

tasks = {
    0: {
        "id":0,
        "description": "homework",
        "done": False,
    },
    
    1: {
        "id": 1,
        "description": "testing",
        "done": False,
    }
}

task_id_counter = 2


@app.route("/tasks/")
def get_tasks():
    data = list(tasks.values())
    response = {
        "success": True,
        "data": data,
    }
    return json.dumps(response), 200
    
@app.route("/tasks/", methods=["POST"])
def create_task():
    global task_id_counter
    body = json.loads(request.data)
    description = body.get("description")
    task = {
        "id": task_id_counter,
        "description": description,
        "done": False
    }
    tasks[task_id_counter] = task
    task_id_counter += 1
    return json.dumps({"success": True, "data": task}), 201

@app.route("/tasks/<int:task_id>/", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"success": False, "error": "Task not found!"}), 404
    return json.dumps({"success": True, "data": task }), 200


@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"success": False, "error": "task not found!"}), 404
    body = json.loads(request.data)
    task["description"] = body.get("description")
    task["done"] = body.get("done")
    return json.dumps({"success": True, "data": task}), 200
    

@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = tasks.get(task_id, None) # can remove None by default
    if not task:
        return json.dumps({"success": False, "error": "Task not found!"}), 404
    del tasks[task_id]
    return json.dumps({"success": True, "data": task}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
