from flask import Flask
import db

DB = db.DatabaseDriver()

app = Flask("__main__")

@app.route("/")
def hello():
    return "Airbnb Admin"

@app.route("/bookings/")
def get_bookings():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)