from flask import Blueprint, jsonify
from app.models import (
    User
)

user = Blueprint("user", __name__)

@user.route("/user/<userid>")
def is_user(userid):
    user = User.query.filter(User.id == userid).first()
    if not user:
        return jsonify({"user": False})
    return jsonify({"user": True})
