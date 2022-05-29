from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import movie_schema
from implemented import movie_service
from views.decorators import auth_required, admin_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        all_movies = movie_service.get_all(filters)
        res = movie_schema.dump(all_movies, many=True)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        print(movie)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid):
        data = request.json
        data["id"] = mid
        movie_service.update(data)
        return "", 204

    @admin_required
    def delete(self, mid):
        movie_service.delete(mid)
        return "", 204
