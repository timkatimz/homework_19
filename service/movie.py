from marshmallow import ValidationError

from dao.model.movie import movie_schema
from dao.model.user import user_schema
from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self, filters):
        if filters.get("director_id") is not None:
            movies = self.dao.get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = self.dao.get_by_genre_id(filters.get("genre_id"))
        elif filters.get("year") is not None:
            movies = self.dao.get_by_year(filters.get("year"))
        else:
            movies = self.dao.get_all()
        return movies

    def create(self, data):
        try:
            movie_schema.load(data)
        except ValidationError as e:
            return f"{e}"
        return self.dao.create(data)

    def update(self, data):
        try:
            movie_schema.load(data)
        except ValidationError as e:
            return f"{e}"
        movie = self.get_one(data.get("id"))
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")
        return self.dao.update(movie)


    def delete(self, mid):
        self.dao.delete(mid)
