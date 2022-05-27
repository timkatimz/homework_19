from marshmallow import ValidationError

from dao.director import DirectorDAO
from dao.model.director import director_schema


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, did):
        return self.dao.get_one(did)

    def get_all(self):
        return self.dao.get_all()

    def create(self, director_d):
        try:
            director_schema.load(director_d)
        except ValidationError as e:
            return f"{e}"
        return self.dao.create(director_d)

    def update(self, director_d):
        try:
            director_schema.load(director_d)
        except ValidationError as e:
            return f"{e}"
        did = director_d.get("id")
        director = self.get_one(did)
        director.name = director_d.get("name")
        return self.dao.update(director)

    def delete(self, did):
        return self.dao.delete(did)
