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

@app.route("/products/")
def get_products():
    data = list(products.values())
    if not data:
        return json.dumps({"success": False, "error": "Products not found!"}), 404
    return json.dumps({"success": True, "data": data}), 200

@app.route("/products/<int:product_id>/")
def get_product_by_id(product_id):
    product = products.get(product_id)
    if not product:
        return json.dumps({"success": False, "error": "Product not found!"})
    return json.dumps({"success": True, "data": product})
    
@app.route("/cart/")
def get_cart():
    data = list(cart.values())
    if cart_item_count == 0:
        return json.dumps({"data": "cart is empty!"}),200
    return json.dumps({"success": True, "data": data}),200

@app.route("/cart/", methods=["POST"])
def add_product_to_cart():
    global cart_item_count
    body = json.loads(request.data)
    product_id = body.get("id")
    product = products.get(product_id)
    
    if not product:
        return json.dumps({"success": False, "error": "Product not found!"}), 404
    
    item = {
        "id": product_id,
        "name": product.get("name"),
        "price": product.get("price"),
        "quantity": product.get("quantity")
    }
    if not item:
        return json.dumps({"success": False, "data": "item not found!"}), 404
    cart[cart_item_count] = item
    cart_item_count += 1 
    print(cart_item_count)
    return json.dumps({"success": True, "data": item}), 201
        
@app.route("/cart/", methods=["DELETE"])
def delete_cart_product():
    body = json.loads(request.data)
    product_id = body.get("id")
    product = products.get(product_id)
    
    if not product:
        return json.dumps({"success": False, "error": "Product not found!"}), 404
    
    item = {
        "id": product_id,
        "name": product.get("name"),
        "price": product.get("price"),
        "quantity": product.get("quantity")
    }
    
    if not item:
        return json.dumps({"sucess": False, "data": "item not found!"}), 404
    
    del cart[product_id] 
    return json.dumps({"success": True, "data": item}),200    
     
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)