# Load environment variable from .env file
from dotenv import load_dotenv
load_dotenv(".env")

# Create global app object
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__, instance_relative_config=True)

# Load security measure
from app.security.authorization import basic_auth
@app.before_request
@basic_auth.login_required
def nothing_func():
    return None

# Login into Gmail Server
# from app.utils.email_authorization import gmail_server

# Change configuration file by searching environment
from config.config import configs
env = "dev"
if app.config["ENV"] == "ProductionConfig":
    env = "prod"
app.config.from_object(configs[env])

# Register the blueprint and apply CORS app
from app.views import blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint)

CORS(app)
