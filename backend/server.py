from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_connection import get_sql_connection
import json

import products_dao
import order_dao
import uom_dao

app = Flask(__name__)
CORS(app)

# Database Connection
connection = get_sql_connection()

# Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Grocery Store Management System API is running successfully!",
        "status": "success"
    })


# Get UOM
@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    return jsonify(response)


# Get Products
@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    return jsonify(response)


# Insert Product
@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])

    product_id = products_dao.insert_new_product(
        connection,
        request_payload
    )

    return jsonify({
        "product_id": product_id,
        "message": "Product inserted successfully"
    })


# Get All Orders
@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = order_dao.get_all_orders(connection)
    return jsonify(response)


# Insert Order
@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])

    order_id = order_dao.insert_order(
        connection,
        request_payload
    )

    return jsonify({
        "order_id": order_id,
        "message": "Order inserted successfully"
    })


# Delete Product
@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    product_id = request.form['product_id']

    deleted = products_dao.delete_product(
        connection,
        product_id
    )

    return jsonify({
        "product_id": deleted,
        "message": "Product deleted successfully"
    })


# Run Server
if __name__ == "__main__":
    print("=========================================")
    print(" Grocery Store Management System API")
    print(" Server Started Successfully")
    print(" http://127.0.0.1:5000")
    print("=========================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )