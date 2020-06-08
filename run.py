from commands.setup import setup_env
setup_env()

from app import app
from app.models import db
from flask_cors import CORS
import pymysql

pymysql.install_as_MySQLdb()
app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
