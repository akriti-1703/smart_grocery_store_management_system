from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

from sql_connection import get_sql_connection
import products_dao
import order_dao
import uom_dao

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

# Database Connection
connection = get_sql_connection()


# ---------------- FRONTEND ROUTES ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manage-product")
def manage_product():
    return render_template("manage-product.html")


@app.route("/order")
def order():
    return render_template("order.html")


# ---------------- API ROUTES ----------------

@app.route("/getUOM", methods=["GET"])
def get_uom():
    return jsonify(uom_dao.get_uoms(connection))


@app.route("/getProducts", methods=["GET"])
def get_products():
    return jsonify(products_dao.get_all_products(connection))


@app.route("/insertProduct", methods=["POST"])
def insert_product():

    request_payload = json.loads(request.form["data"])

    product_id = products_dao.insert_new_product(
        connection,
        request_payload
    )

    return jsonify({
        "product_id": product_id,
        "message": "Product inserted successfully"
    })


@app.route("/deleteProduct", methods=["POST"])
def delete_product():

    product_id = request.form["product_id"]

    deleted = products_dao.delete_product(
        connection,
        product_id
    )

    return jsonify({
        "product_id": deleted,
        "message": "Product deleted successfully"
    })


@app.route("/getAllOrders", methods=["GET"])
def get_all_orders():
    return jsonify(order_dao.get_all_orders(connection))


@app.route("/insertOrder", methods=["POST"])
def insert_order():

    request_payload = json.loads(request.form["data"])

    order_id = order_dao.insert_order(
        connection,
        request_payload
    )

    return jsonify({
        "order_id": order_id,
        "message": "Order inserted successfully"
    })


# ---------------- ERROR HANDLER ----------------

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "error": str(e)
    }), 500


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )