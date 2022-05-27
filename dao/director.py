from dao.model.director import Director
from sqlalchemy.exc import NoResultFound


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, did):
        try:
            director = self.session.query(Director).filter(Director.id == did).one()
        except NoResultFound as e:
            return f"{e}"
        return director

    def get_all(self):
        return self.session.query(Director).all()

    def create(self, director_d):
        ent = Director(**director_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, did):
        director = self.get_one(did)
        self.session.delete(director)
        self.session.commit()

    def update(self, director_d):
        self.session.add(director_d)
        self.session.commit()
