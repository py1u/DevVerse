from flask import Flask, request
import json

app = Flask(__name__)

products = {
    0: {
        "id": 0,
        "name": "Macbook Pro 14in 2023",
        "price": 1799,
        "description": "The Macbook Pro is a high performance laptop ideal for machine learning and computational tasks.",
    },
    1: {
        "id": 1,
        "name": "Iphone 16",
        "price": 899,
        "description": "The Iphone 16 is the latest iphone released by Apple in September 2024.",
    },
    2: {
        "id": 2,
        "name": "Apple Watch 2",
        "price": 299,
        "description": "The Apple Watch 2 is a smart watch that can help track your lifestyle and fitness.",
    }

}

cart = {}

product_id_count = 3
cart_item_count = 0

@app.route("/")
def hello():
    return "Hello, World!"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)