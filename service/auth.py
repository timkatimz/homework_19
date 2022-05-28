import calendar
import datetime
import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET, ALGORITHM
import jwt

from flask_restx import abort

from dao.auth import AuthDAO


class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def create(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        if None in [username, password]:
            abort(401)

        user = self.dao.get_by_username(username)
        if user is None:
            abort(401)

        password = self.hash_password(password)
        if password != user.password:
            abort(403)

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    def update(self, data):
        refresh_token = data.get("refresh_token")
        if refresh_token is None:
            abort(401)

        try:
            jwt.decode(refresh_token=refresh_token, key=SECRET, algorithm=ALGORITHM)
        except Exception:
            abort(403)

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    def hash_password(self, password):
        pwd = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
        return pwd
