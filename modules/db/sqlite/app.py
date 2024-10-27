from flask import Flask

app = Flask("__name__")

@app.route("/")
def hello():
    return "Hello World!"


def sucess_res(data, code=200):
    pass

def failure_res(message, code=404):
    pass

@app.route("/tasks/")
def get_tasks():
    pass

@app.route("tasks/", methods=["POST"])
def create_task():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
