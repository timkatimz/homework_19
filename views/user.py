from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import user_schema
from implemented import user_service

user_ns = Namespace("users")


@user_ns.route("/")
class UsersView(Resource):
    def get(self):
        users = user_service.get_all()
        return user_schema.dump(users, many=True), 200

    def post(self):
        user = request.json
        user_service.create(user)
        return "Created", 201


@user_ns.route("/<int:uid>")
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        return user_schema.dump(user), 200

    def put(self, uid):
        data = request.json
        data["id"] = uid
        user_service.update(data)
        return "Updated", 201

    def delete(self, uid):
        user_service.delete(uid)
        return "Deleted", 204
