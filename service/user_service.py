from sqlalchemy.exc import IntegrityError

from main import db
from model.user import User


def create_user(user: User) -> bool:
    db.session.add(user)
    try:
        db.session.commit()
        return True
    except IntegrityError as ex:
        db.session.rollback()
        print(ex)
        return False
    return False


def get_user(email_id: str) -> User:
    return User.query.filter_by(email_id=email_id).first()
