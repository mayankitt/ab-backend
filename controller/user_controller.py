from flask import Blueprint

user_controller = Blueprint('user', __name__, url_prefix='/api/user')


@user_controller.route('/say_hello')
def say_hello():
    return 'Hello!'


@user_controller.route('/create_dummy_user')
def create_dummy_user():
    from model.user import User
    u = User()
    u.email_id = 'mayankitt@yahoo.com'
    u.password_hash = 'dummy_hash'
    from service.user_service import create_user
    return "Success" if create_user(u) else "Failed"
