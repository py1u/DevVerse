from flask import Flask
import db
import json

DB = db.DatabaseDriver()

app = Flask("__main__")

@app.route("/")
def hello():
    return "Airbnb Admin"

@app.route("/bookings/")
def get_bookings():
    data = DB.get_booking_table()
    return json.dumps({"success": True, "data": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)