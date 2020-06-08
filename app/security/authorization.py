import os
from flask_httpauth import HTTPBasicAuth

http_username = os.environ.get("USERNAME_AUTHORIZATION")
http_password = os.environ.get("PASSWORD_AUTHORIZATION")
basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    print(username, http_username, password, http_password)
    if username == http_username and password == http_password:
        return username
