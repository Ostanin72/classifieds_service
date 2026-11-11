from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from db import Posting, Session, User
from errors import HttpError
from schema import (
    CreatePosting,
    CreateUser,
    UpdatePosting,
    UpdateUser,
    validate,
    validate_posting,
)

app = Flask("app")

bcrypt = Bcrypt(app)


def hash_password(password):
    password = password.encode("utf-8")
    password = bcrypt.generate_password_hash(password)
    password = password.decode("utf-8")
    return password


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"message": str(error)})
    response.status_code = error.status_code
    return response


def get_user(user_id: int) -> User:
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError("User not found", 404)
    return user


def add_user(user: User):
    request.session.rollback()
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError("User already exists", 409)


class UserView(MethodView):
    def get(self, user_id):
        user = get_user(user_id)
        return jsonify(user.user_dict)

    def post(self):
        json_data = validate(request.json, CreateUser)
        user = User(
            username=json_data["username"],
            password=hash_password(json_data["password"]),
            email=json_data["email"],
        )
        add_user(user)
        return jsonify(user.user_dict)

    def patch(self, user_id):
        json_data = validate(request.json, UpdateUser)
        user = get_user(user_id)

        if "username" in json_data:
            user.username = json_data["username"]
        if "password" in json_data:
            user.password = hash_password(json_data["password"])
        add_user(user)
        return jsonify(user.user_dict)

    def delete(self, user_id):
        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"message": "User deleted"})


user_view = UserView.as_view("user")


def get_posting(posting_id: int) -> Posting:
    posting = request.session.get(Posting, posting_id)
    if posting is None:
        raise HttpError("Posting not found", 404)
    return posting


class PostingView(MethodView):
    def get(self, posting_id):
        posting = get_posting(posting_id)
        return jsonify(posting.posting_dict)

    def post(self):
        json_data = validate_posting(request.json, CreatePosting, request.session)

        posting = Posting(
            heading=json_data["heading"],
            description=json_data["description"],
            owner_id=json_data["owner_id"],
        )
        request.session.add(posting)
        request.session.commit()
        return jsonify(posting.posting_dict)

    def patch(self, posting_id):
        json_data = validate_posting(request.json, UpdatePosting, request.session)
        posting = get_posting(posting_id)

        if posting.owner_id != json_data["owner_id"]:
            raise HttpError("Это не Ваше объявление", 403)
        if "heading" in json_data:
            posting.heading = json_data["heading"]
        if "description" in json_data:
            posting.description = json_data["description"]
        request.session.add(posting)
        request.session.commit()
        return jsonify(posting.posting_dict)

    def delete(self, posting_id):
        json_data = validate_posting(request.json, UpdatePosting, request.session)
        posting = get_posting(posting_id)
        if posting.owner_id != json_data["owner_id"]:
            raise HttpError("Это не Ваше объявление", 403)
        request.session.delete(posting)
        request.session.commit()
        return jsonify({"message": "Posting deleted"})


posting_view = PostingView.as_view("posting")

app.add_url_rule("/postings", view_func=posting_view, methods=["POST"])

app.add_url_rule(
    "/postings/<int:posting_id>",
    view_func=posting_view,
    methods=["GET", "PATCH", "DELETE"],
)

app.add_url_rule("/users", view_func=user_view, methods=["POST"])

app.add_url_rule(
    "/users/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)

app.run()
