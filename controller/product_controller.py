from flask import Blueprint, jsonify

product_controller = Blueprint('product', __name__)


@product_controller.route('/get_all')
def get_all_products():
    response = {
        "message": "Hello"
    }
    return jsonify(response)
