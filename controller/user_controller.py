import datetime

import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from controller import token_required
from main import app
from model.user import User

user_controller = Blueprint('user', __name__, url_prefix='/api/user')


@user_controller.route('/say_hello', methods=['GET'])
def say_hello():
    return 'Hello!'


@user_controller.route('/create_dummy_user', methods=['GET'])
def create_dummy_user():
    from model.user import User
    u = User()
    u.email_id = 'admin@custom.app'
    u.password_hash = generate_password_hash('dummy_password')
    from service.user_service import create_user
    return "Success" if create_user(u) else "Failed"


@user_controller.route('/get_user', methods=['GET'])
@token_required
def get_user_by_email():
    email_id: str = request.args.get('email')
    from service.user_service import get_user
    user: User = get_user(email_id)
    response: dict
    if user is not None:
        response = {
            "user_email":           user.email_id,
            "user_password_hash":   user.password_hash
        }
    else:
        response = {
            "error": "User not found."
        }
    return jsonify(response)


@user_controller.route('/login', methods=['POST'])
def authenticate_user():
    supplied_credentials: dict = request.get_json()
    from service.user_service import get_user
    user_being_authenticated: User = get_user(supplied_credentials['email'])
    error_response: dict = {
            'error': 'Incorrect credentials supplied.'
        }
    if user_being_authenticated is None or \
            not check_password_hash(user_being_authenticated.password_hash, supplied_credentials['password']):
        return jsonify(error_response)
    else:
        token_expiration = (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).timestamp()
        token = jwt.encode({
            'user_email': user_being_authenticated.email_id,
            'generated_on': datetime.datetime.utcnow().timestamp(),
            'expiration': token_expiration
        }, app.config['SECRET_JWT_KEY'])
        return jsonify({
            'message': 'User authenticated. Please pass this token for authorization in all subsequent requests.',
            'token': token,
            'expiry': token_expiration
        })

