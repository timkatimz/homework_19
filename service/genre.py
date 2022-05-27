from marshmallow import ValidationError

from dao.genre import GenreDAO
from dao.model.genre import genre_schema


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid):
        return self.dao.get_one(gid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, genre_d):
        try:
            genre_schema.load(genre_d)
        except ValidationError as e:
            return f"{e}"
        return self.dao.create(genre_d)

    def update(self, genre_d):
        try:
            genre_schema.load(genre_d)
        except ValidationError as e:
            return f"{e}"
        did = genre_d.get("id")
        genre = self.get_one(did)
        genre.name = genre_d.get("name")
        return self.dao.update(genre)

    def delete(self, gid):
        return self.dao.delete(gid)
