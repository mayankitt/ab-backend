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

