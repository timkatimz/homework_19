from flask import request, abort
import jwt
from constants import SECRET, ALGORITHM


def auth_required(func):
    def wrapper(*args, **kwargs):
        try:
            data = request.headers["Authorization"]
        except Exception as e:
            return f"Authorization error: {e}", 401
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        except Exception as e:
            return f"JWT decode error: {e}"
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        try:
            data = request.headers["Authorization"]
        except Exception as e:
            return f"Authorization error: {e}", 401
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        except Exception as e:
            return f"JWT decode error: {e}"

        if user["role"] != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper
