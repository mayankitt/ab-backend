from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_JWT_KEY'] = 'my-secret-key'
db = SQLAlchemy(app)

if __name__ == '__main__':
    from controller.user_controller import user_controller
    from controller.product_controller import product_controller
    app.register_blueprint(user_controller)
    app.register_blueprint(product_controller)
    app.run('0.0.0.0')

