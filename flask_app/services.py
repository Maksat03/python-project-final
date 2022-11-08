import jwt
from .app import app
from flask import request as HttpRequest
from typing import Mapping, Union, Tuple
from database.models import User, save_obj
from database.db import session


def get_request_user(request: HttpRequest) -> Union[User, None]:
    session_id = request.cookies.get("session_id", "no_session_id")
    return session.query(User).filter_by(session_id=session_id).first()


def request_is_authenticated(request: HttpRequest) -> bool:
    session_id = request.cookies.get("session_id", "")
    if session_id:
        return session.query(User).filter_by(session_id=session_id).count()
    return False


def user_login(form: Mapping) -> Tuple[bool, str]:
    password = jwt.encode({"password": form["password"]}, app.config["SECRET_KEY"], algorithm="HS256")
    user = session.query(User).filter_by(username=form["username"], password=password).first()

    if user:
        user.session_id = jwt.encode({"uid": user.id}, app.config["SECRET_KEY"], algorithm="HS256")
        save_obj(user)
        return True, user.session_id

    return False, ""


def user_register(form: Mapping) -> bool:
    username = form["username"]
    password1 = form["password1"]
    password2 = form["password2"]

    if password1 == password2:
        user = session.query(User).filter_by(username=username).first()

        if user:
            return False

        password = jwt.encode({"password": password1}, app.config["SECRET_KEY"], algorithm="HS256")
        user = User(username=username, password=password)
        save_obj(user)
        return True

    return False


def user_logout(request: HttpRequest) -> None:
    user = get_request_user(request)
    user.session_id = None
    save_obj(user)
