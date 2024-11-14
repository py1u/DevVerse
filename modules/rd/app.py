from flask import Flask, request
import json
import db

app = Flask("__main__")

DB = db.DatabaseDriver()

@app.route("/")
def home():
    return "Hello World!"

@app.route("/tasks/")
def get_all_tasks():
    data =  DB.get_all_tasks();
    return json.dumps({"success": True, "data": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    
    