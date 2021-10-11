from sqlalchemy.exc import IntegrityError

from main import db
from model.product import Product


def create_product(product: Product) -> bool:
    last_product = get_last_inserted_product()
    if last_product is None:
        product.product_id = 'P001'
    else:
        product.product_id = 'P' + str(int(last_product.id) + 1).zfill(3)
    db.session.add(product)
    try:
        db.session.commit()
        return True
    except IntegrityError as ex:
        db.session.rollback()
        return False


def get_product(product_id: str) -> Product:
    return Product.query.filter_by(product_id=product_id).first()


def get_last_inserted_product() -> Product:
    return Product.query.order_by(Product.id.desc()).first()


def get_products():
    return Product.query.all()


def get_products_by_category(category: str) -> list:
    return Product.query.filter_by(product_category=category).all()


def delete_product(product_id: str):
    product = get_product(product_id)
    if product is None:
        return False
    else:
        try:
            db.session.delete(product)
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
            db.session.rollback()
            return False


def update_product(product_id, name=None, description=None, category=None, units=None) -> bool:
    product = db.session.query(Product).filter(Product.product_id == product_id).one()
    if product is None:
        return False
    else:
        product.name = name if name is not None else product.product_name
        product.product_description = description if description is not None else product.product_description
        product.product_category = category if category is not None else product.product_category
        product.units = units if units is not None else product.units
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


def validate_product_id(provided_id: str, required=True) -> list:
    error_messages: list = []
    if required and (provided_id is None or len(provided_id) == 0):
        error_messages.append('Product ID cannot be empty.')
    elif provided_id is None:
        return error_messages
    return error_messages


def validate_product_name(provided_name: str, required=False) -> list:
    error_messages: list = []
    if required and (provided_name is None or len(provided_name) == 0):
        error_messages.append('Product Name cannot be empty.')
        return error_messages
    elif provided_name in None:
        return error_messages
    if len(provided_name) == 0:
        error_messages.append('Product Name can\'t be an empty string')
    if len(provided_name) > 50:
        error_messages.append('Name of the product cannot exceed 50 characters.')
    if string_contains_special_characters(provided_name):
        error_messages.append('Name of the product cannot contain special characters.')
    return error_messages


def validate_product_description(provided_description: str, required=False) -> list:
    error_messages: list = []
    if required and (provided_description is None or len(provided_description) == 0):
        error_messages.append('Product Category cannot be empty.')
        return error_messages
    elif provided_description is None:
        return error_messages
    if len(provided_description) > 200:
        error_messages.append('Description of the product cannot exceed 200 characters.')
    if string_contains_special_characters(provided_description):
        error_messages.append('Description of the product cannot contain special characters.')
    return error_messages


def validate_category(provided_category: str, required=False) -> list:
    error_messages: list = []
    if required and (provided_category is None or len(provided_category) == 0):
        error_messages.append('Product Category cannot be empty.')
        return error_messages
    elif provided_category is None:
        return error_messages
    categories: list = [
        'SPACE',
        'HELICOPTER',
        'COMMERCIAL'
    ]
    if provided_category not in categories:
        error_messages.append(
            'Value \'%s\' for category not valid. Possible values: %s', (provided_category, categories))
    return error_messages


def validate_units(provided_units: int, required=False) -> list:
    error_list: list = []
    if required and provided_units is None:
        error_list.append('Product Units cannot be empty.')
        return error_list
    elif provided_units is None:
        return  error_list
    if provided_units < 0:
        error_list.append('Product units value cannot be less than 0')


def string_contains_special_characters(string: str) -> bool:
    import re
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    return True if regex.search(string) else False
