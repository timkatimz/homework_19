import hashlib

from dao.model.user import user_schema
from dao.user import UserDAO
from marshmallow import ValidationError
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        try:
            user_schema.load(data)
        except ValidationError as e:
            return f"{e}"
        password = self.hash_password(data.get("password"))
        data["password"] = password
        return self.dao.create(data)

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def update(self, data):
        try:
            user_schema.load(data)
        except ValidationError as e:
            return f"{e}"
        uid = data.get("id")
        user = self.dao.get_one(uid)
        user.username = data.get("username")
        user.password = self.hash_password(data.get("password"))
        user.role = data.get("role")
        self.dao.update(user)

    def delete(self, uid):
        return self.dao.delete(uid)

    def hash_password(self, password):
        pwd = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
        return pwd
