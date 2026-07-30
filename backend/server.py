from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import json

import products_dao
import order_dao
import uom_dao

app = Flask(__name__)


connection = get_sql_connection()


@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = jsonify(uom_dao.get_uom(connection))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getProducts', methods=['GET'])
def get_products():
    response = jsonify(products_dao.get_all_products(connection))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)

    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    result = products_dao.delete_product(
        connection,
        request.form['product_id']
    )

    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = jsonify(order_dao.get_all_orders(connection))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])

    order_id = order_dao.insert_order(
        connection,
        request_payload
    )

    response = jsonify({
        'order_id': order_id
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# ============================
# NEW DELETE ORDER API
# ============================

@app.route('/deleteOrder', methods=['POST'])
def delete_order():

    order_id = request.form['order_id']

    result = order_dao.delete_order(connection, order_id)

    response = jsonify(result)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)