from main import db
from model.user import User


def create_user(user: User):
    db.session.add(user)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
