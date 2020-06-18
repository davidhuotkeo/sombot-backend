from flask import Blueprint, jsonify, request, abort
from app.models import User
from app.controllers.database_controllers import (
    hash_password,
    verify_password,
    add_to_database
)
from app.controllers.cleaner import name_cleaner
import os

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=["POST"])
def login():
    # get the json data request
    login_request = request.json

    # if the request is hacked without data
    if not login_request:
        return abort(403)

    # get the email from json data
    email = login_request.get('email')
    password = login_request.get('password')

    # read from database where email the same
    existing_user = User.query.filter(User.email == email).first()

    # if not exist return a json with id of null object
    if not existing_user:
        return jsonify({"id": None}), 404

    if password == None:
        return jsonify({'id': existing_user.id}), 200

    # get the password hashed from database
    # and verify the user password
    hashed_password = existing_user.password
    is_user = verify_password(hashed_password, password)
    
    # return id as data
    if not is_user:
        return jsonify({'id': None}), 401

    return jsonify({'id': existing_user.id}), 200

@auth.route('/signup', methods=["POST"])
def signup():
    # get request data if not abort
    signup_request = request.json
    if not signup_request:
        return abort(403)

    # getting data
    email = request.json.get("email")
    password = request.json.get("password")

    # read data from database
    existing_user = User.query.filter(User.email == email).first()
    if existing_user:
        return jsonify({'id': None}), 403
    
    # hash and store to database
    hashed_password = hash_password(password)
    name = name_cleaner(email)
    new_user = User(email, hashed_password, name)
    add_to_database(new_user)

    return jsonify({'id': new_user.id}), 200

@auth.route('/google_auth', methods=['POST'])
def google():
    data = request.json
    email = data.get('email')

    exist_user = User.query.filter(User.email == email).first()
    if exist_user:
        return jsonify({'id': exist_user.id}), 200

    password = os.environ.get("DEFAULT_PASSWORD")

    name = name_cleaner(email)
    hashed_password = hash_password(password)
    user = User(email, password, name)
    add_to_database(user)

    return jsonify({'id': user.id}), 200
