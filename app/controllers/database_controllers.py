from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db
from uuid import uuid4
from datetime import datetime

def add_to_database(db_obj):
    """
    add to database with database object

    Args:
    - db_obj: Any Class Object
    """
    db.session.add(db_obj)
    db.session.commit()

def generate_id():
    """
    Generate ID from uuid hex
    """
    uuid_obj = uuid4()
    string_hex = uuid_obj.hex.upper()
    return string_hex

# LAMDA FUNCTION
# hash the password
hash_password = lambda password: generate_password_hash(password)
# confirm if the password is matched or not
verify_password = lambda hashed_password, input_password: check_password_hash(hashed_password, input_password)
# get now date
get_now_date = lambda : datetime.now()
# convert from string to datetime
from_string_to_date = lambda date: datetime.strptime(date, "%d-%m-%Y %H:%M")
