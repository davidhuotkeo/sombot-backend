import os
from app import app

db = {
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "db": os.getenv("DB_NAME")
}
DB_URI = "mysql://{}:{}@{}/{}".format(db["username"], db["password"], db["host"], db["db"])

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_FOLDER = app.root_path + "/csv"

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

configs = {
    "default": BaseConfig,
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}