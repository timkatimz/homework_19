from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import director_schema
from implemented import director_service

director_ns = Namespace('directors')



@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = director_service.get_all()
        return director_schema.dump(directors, many=True), 200

    def post(self):
        director = request.json
        director_service.create(director)
        return "Created", 201


@director_ns.route("/<int:did>")
class DirectorView(Resource):
    def get(self, did):
        director = director_service.get_one(did)
        return director_schema.dump(director), 200

    def put(self):
        data = request.json
        director_service.update(data)
        return "Updated", 201

    def delete(self, did):
        director_service.delete(did)
        return "Deleted", 204
