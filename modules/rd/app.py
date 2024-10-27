from flask import Flask, request
import json

app = Flask(__name__)

# python dictionaries
# key : value pairs -> JSON syntax

users = {
    0: {
    "id": 0,
    "name": "Peter",
    "email": "plu040@ucr.edu",
    "age": 21
    },
    
    1: {
    "id": 1,
    "name": "Hao",
    "email": "hmai015@ucr.edu",
    "age": 22
    },
    2: {
    "id": 2,
    "name": "Jenny",
    "email": "jquan026@ucr.edu",
    "age": 22
    }
}


user_id_count = 3


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/users/")
def get_users():
    data = list(users.values())
    if not data:
        return json.dumps({"success": False, "error": "users not found!"}), 404
    return json.dumps({"success": True, "data": data}),200 

@app.route("/users/<int:user_id>/")
def get_user_by_id(user_id):
    user = users.get(user_id)
    if not user:
        return json.dumps({"success": False, "error": "user not found!"}), 404
    return json.dumps({"success": True, "data": user}), 200

@app.route("/users/", methods=["POST"])
def create_user():
    global user_id_count
    body = json.loads(request.data)
    nm = body.get("name")
    email = body.get("email")
    age = body.get("age")
    user = {
        "id": user_id_count,
        "name": nm,
        "email": email,
        "age": age,
    }
    users[user_id_count] = user
    user_id_count += 1
    return json.dumps({"success": True, "data": user}), 200

@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user_by_id(user_id):
    user = users.get(user_id, None)
    if not user:
        return json.dumps({"success": False, "error": "user not found!"}), 404
    del users[user_id]
    return json.dumps({"success": True, "data": user}),200

@app.route("/users/<int:user_id>/", methods=["POST"])
def update_user_by_id(user_id):
    user = users.get(user_id)
    if not user:
        return json.dumps({"success": False, "error": "user not found!"}), 404
    body = json.loads(request.data)
    nm = body.get("name")
    user["name"] = nm
    return json.dumps({"success": True, "data": user}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


