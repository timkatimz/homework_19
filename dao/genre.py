from sqlalchemy.exc import NoResultFound
from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, gid):
        try:
            genre = self.session.query(Genre).filter(Genre.id == gid).one()
        except NoResultFound as e:
            return f"{e}"
        return genre

    def get_all(self):
        return self.session.query(Genre).all()

    def create(self, genre_d):
        ent = Genre(**genre_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, gid):
        genre = self.get_one(gid)

        self.session.delete(genre)
        self.session.commit()

    def update(self, genre_d):
        self.session.add(genre_d)
        self.session.commit()
