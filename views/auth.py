from flask import request
from flask_restx import Namespace, Resource

from implemented import auth_service

auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        data = request.json
        return auth_service.create(data)

    def put(self):
        data = request.json
        return auth_service.update(data)
