from sqlalchemy import Column, String

from main import db


class User(db.Model):
    __tablename__ = 'users'
    email_id = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
