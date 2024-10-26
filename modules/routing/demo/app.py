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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
