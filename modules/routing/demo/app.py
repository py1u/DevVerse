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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
