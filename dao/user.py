from sqlalchemy.exc import NoResultFound

from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        new_user = User(**data)

        self.session.add(new_user)
        self.session.commit()

    def get_one(self, uid):
        try:
            user = self.session.query(User).filter(User.id == uid).one()
        except NoResultFound as e:
            return f"{e}", 400
        return user

    def update(self, user):
        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        try:
            user = self.session.query(User).filter(User.id == uid).one()
        except NoResultFound as e:
            return f"{e}"
        self.session.delete(user)
        self.session.commit()
