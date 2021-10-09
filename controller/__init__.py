from datetime import datetime
from functools import wraps


# decorator for verifying the JWT
import jwt
from flask import request, jsonify, make_response
from jwt import DecodeError

from main import app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        # return 401 if token is not passed
        if not token:
            return make_response(jsonify({'message': 'Token is missing !!'}), 401)

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_JWT_KEY'], algorithms=['HS256'])
            if int(data['expiration']) < int(datetime.utcnow().timestamp()):
                raise DecodeError
        except DecodeError as ex:
            return make_response(jsonify({
                'message': 'Token is invalid or expired !!'
            }), 401)
        return f(*args, **kwargs)

    return decorated
