from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

from backend.sql_connection import get_sql_connection
from backend import products_dao
from backend import order_dao
from backend import uom_dao

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

# Database Connection



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
    connection = get_sql_connection()
    try:
        return jsonify(uom_dao.get_uoms(connection))
    finally:
        connection.close()


@app.route("/getProducts", methods=["GET"])
def get_products():
    connection = get_sql_connection()
    try:
        return jsonify(products_dao.get_all_products(connection))
    finally:
        connection.close()


@app.route("/insertProduct", methods=["POST"])
def insert_product():
    connection = get_sql_connection()
    try:
        request_payload = json.loads(request.form["data"])
        product_id = products_dao.insert_new_product(connection, request_payload)

        return jsonify({
            "product_id": product_id,
            "message": "Product inserted successfully"
        })
    finally:
        connection.close()

@app.route("/deleteProduct", methods=["POST"])
def delete_product():
    connection = get_sql_connection()
    try:
        product_id = request.form["product_id"]

        deleted = products_dao.delete_product(
            connection,
            product_id
        )

        return jsonify({
            "product_id": deleted,
            "message": "Product deleted successfully"
        })
    finally:
        connection.close()


@app.route("/getAllOrders", methods=["GET"])
def get_all_orders():
    connection = get_sql_connection()
    try:
        return jsonify(order_dao.get_all_orders(connection))
    finally:
        connection.close()

@app.route("/insertOrder", methods=["POST"])
def insert_order():
    connection = get_sql_connection()

    try:
        request_payload = json.loads(request.form["data"])

        order_id = order_dao.insert_order(
            connection,
            request_payload
        )

        return jsonify({
            "order_id": order_id,
            "message": "Order inserted successfully"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        connection.close()
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