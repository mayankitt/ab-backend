from flask import Blueprint, jsonify, request, make_response

from controller import token_required
from model.product import Product
from service.product_service import get_products, create_product, get_product, get_products_by_category, delete_product, \
    update_product

product_controller = Blueprint('product', __name__, url_prefix='/api/product')


@product_controller.route('/get_all', methods=['GET'])
@token_required
def get_all_products():
    return jsonify([product.to_dictionary() for product in get_products()])


@product_controller.route('/create', methods=['POST'])
@token_required
def create_new_product():
    product_details = request.get_json()
    product = Product()
    product.product_name = product_details['name']
    product.product_description = product_details['description']
    product.product_category = product_details['category']
    product.units = product_details['units']
    product_created = create_product(product)
    if product_created:
        return make_response(
            jsonify({
                'message': 'Product successfully created in system'
            }), 200
        )
    else:
        return make_response(
            jsonify({
                'message': 'The product could not be created in the system.'
            }), 400
        )


@product_controller.route('/get_product', methods=['GET'])
@token_required
def get_product_by_id():
    product_id = request.args.get('id')
    product = get_product(product_id)
    if product is not None:
        return make_response(
            jsonify(product.to_dictionary()), 200
        )
    else:
        return make_response(
            jsonify({
                'message': 'Product not found'
            }), 404
        )


@product_controller.route('/get_by_category', methods=['GET'])
@token_required
def get_product_by_category():
    product_category = request.args.get('category')
    products = get_products_by_category(product_category)
    if len(products) > 0:
        return make_response(
            jsonify([product.to_dictionary() for product in products]), 200
        )
    else:
        return make_response(
            jsonify({
                'message': 'Product(s) not found'
            }), 404
        )


@product_controller.route('/delete', methods=['POST'])
@token_required
def delete_product_by_product_id():
    product_id = request.get_json()['id']
    if delete_product(product_id):
        return make_response(
            jsonify({
                'message': 'Product deleted from system'
            }), 200
        )
    else:
        return make_response(
            jsonify({
                'message': 'Product could not be deleted from system'
            }), 500
        )


@product_controller.route('/update', methods=['PUT'])
@token_required
def update_product_by_id():
    request_body: dict = request.get_json()
    product_id = request_body['id']
    name = request_body['name'] if 'name' in request_body.keys() else None
    description = request_body['description'] if 'description' in request_body.keys() else None
    category = request_body['category'] if 'category' in request_body.keys() else None
    units = request_body['units'] if 'units' in request_body.keys() else None
    if update_product(product_id, name, description, category, units):
        return make_response(
            jsonify({
                'message': 'Product updated'
            }), 201
        )
    else:
        return make_response(
            jsonify({
                'message': 'Product could not be updated'
            }), 500
        )