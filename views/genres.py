from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import genre_schema
from implemented import genre_service
from views.decorators import auth_required, admin_required

genre_ns = Namespace('genres')


@genre_ns.route("/")
class GenresView(Resource):
    @auth_required
    def get(self):
        genres = genre_service.get_all()
        return genre_schema.dump(genres, many=True), 200

    @admin_required
    def post(self):
        genre = request.json
        genre_service.create(genre)
        return "Created", 201


@genre_ns.route("/<int:gid>")
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        genre = genre_service.get_one(gid)
        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, gid):
        data = request.json
        data["id"] = gid
        genre_service.update(data)
        return "Updated", 201

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return "Deleted", 204
