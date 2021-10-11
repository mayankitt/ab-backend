from flask import Blueprint, jsonify, request, make_response

from controller import token_required
from model.product import Product
from service.product_service import get_products, create_product, get_product, get_products_by_category, delete_product, \
    update_product, validate_product_name, validate_product_description, validate_category, validate_units, \
    validate_product_id

product_controller = Blueprint('product', __name__, url_prefix='/api/product')
categories: list = [
    'SPACE',
    'HELICOPTER',
    'COMMERCIAL'
]


@product_controller.route('/get_all', methods=['GET'])
@token_required
def get_all_products():
    return jsonify({
        'message': 'Product list rendered',
        'hasErrors': False,
        'errors': [],
        'data': [product.to_dictionary() for product in get_products()]
    })


@product_controller.route('/create', methods=['POST'])
@token_required
def create_new_product():
    product_details: dict = request.get_json()
    product = Product()
    product.product_name = product_details.get('name')
    product.product_description = product_details.get('description')
    product.product_category = str(product_details['category']).upper() if product_details.get('category') else None
    product.units = product_details.get('units')
    bad_request_errors: list
    bad_request_errors.extend(validate_product_name(product.product_name, True))
    bad_request_errors.extend(validate_product_description(product.product_description, True))
    bad_request_errors.extend(validate_category(product.product_category, True))
    bad_request_errors.extend(validate_units(product.product_units, True))
    if len(bad_request_errors) > 0:
        return make_response({
            jsonify({
                'message': 'Bad Request. Cannot create product.',
                'data': {},
                'hasErrors': True,
                'errors': bad_request_errors
            }), 400
        })
    product_created = create_product(product)
    if product_created:
        return make_response(
            jsonify({
                'message': 'Product successfully created in system',
                'data': {},
                'hasErrors': False,
                'errors': []
            }), 201
        )
    else:
        return make_response(
            jsonify({
                'message': 'The product could not be created in the system.',
                'data': {},
                'hasErrors': True,
                'errors': []
            }), 400
        )


@product_controller.route('/get_product', methods=['GET'])
@token_required
def get_product_by_id():
    product_id = request.args.get('id')
    product = get_product(product_id)
    if product is not None:
        return make_response(
            jsonify({
                'message': 'Product fetched.',
                'data': product.to_dictionary(),
                'hasErrors': False,
                'errors': []
            }), 200
        )
    else:
        return make_response(
            jsonify({
                'message': 'Product not found',
                'data': {},
                'hasError': True,
                'errors': []
            }), 404
        )


@product_controller.route('/get_by_category', methods=['GET'])
@token_required
def get_product_by_category():
    product_category = request.args.get('category')
    products = get_products_by_category(product_category)
    if len(products) > 0:
        return make_response(
            jsonify({
                'message': 'Product(s) retrieved.',
                'data': [product.to_dictionary() for product in products],
                'hasError': False,
                'errors': []
            }), 200
        )
    else:
        return make_response(
            jsonify({
                'message': 'No product(s) not found.',
                'data': {},
                'hasError': True,
                'errors': []
            }), 404
        )


@product_controller.route('/delete', methods=['POST'])
@token_required
def delete_product_by_product_id():
    product_id = request.get_json()['id']
    if delete_product(product_id):
        return make_response(
            jsonify({
                'message': 'Product deleted from system',
                'data': {},
                'hasError': False,
                'errors': []
            }), 200
        )
    else:
        return make_response(
            jsonify({
                'message': 'Product could not be deleted from system',
                'data': {},
                'hasError': True,
                'errors': []
            }), 500
        )


@product_controller.route('/update', methods=['PUT'])
@token_required
def update_product_by_id():
    request_body: dict = dict(request.get_json())
    bad_request_errors: list = list()

    product_id = request_body.get('id')
    bad_request_errors.extend(validate_product_id(product_id))
    name = request_body.get('name')
    bad_request_errors.extend(validate_product_name(name))
    description = request_body.get('description')
    bad_request_errors.extend(validate_product_description(description))
    category = str(request_body['category']).upper() if 'category' in request_body.keys() else None
    bad_request_errors.extend(validate_category(category))
    units = request_body['units'] if 'units' in request_body.keys() else None
    bad_request_errors.extend(validate_units(units))

    if len(bad_request_errors) > 0:
        return make_response(
            jsonify({
                'message': 'Bad Request. Cannot update product.',
                'data': {},
                'hasErrors': True,
                'errors': bad_request_errors
            }), 400
        )
    if update_product(product_id, name, description, category, units):
        return make_response(
            jsonify({
                'message': 'Product updated',
                'data': {},
                'hasError': False,
                'errors': []
            }), 201
        )
    else:
        return make_response(
            jsonify({
                'message': 'Product could not be updated',
                'data': {},
                'hasError': True,
                'errors': []
            }), 500
        )
