from sqlalchemy import Column, String

from main import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
