from flask import Flask

app = Flask("__main__")

@app.route("/")
def hello():
    return "Uber"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)