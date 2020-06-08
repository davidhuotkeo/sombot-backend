from app.models import db
from app.controllers.database_controllers import (
    generate_id,
    get_now_date,
    from_string_to_date
)

class User(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    event = db.relationship("Event", backref="user")

    def __init__(self, email, password, name):
        self.id = generate_id()
        self.email = email
        self.password = password
        self.name = name
        self.date = get_now_date()

class Event(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    name = db.Column(db.String(100))
    body = db.Column(db.String(10_000))
    location = db.Column(db.String(100))
    type = db.Column(db.String(15))
    date = db.Column(db.DateTime)
    user_id = db.Column(db.String(35), db.ForeignKey('user.id'))
    file = db.relationship("File", backref="event")
    audience = db.relationship("Audience", backref="event")

    def __init__(self, event_data, **kwargs):
        self.id = generate_id()
        self.name = event_data.get("name")
        self.body = event_data.get("detail")
        self.location = event_data.get("location")
        self.type = event_data.get("type")
        self.date = from_string_to_date(event_data.get("date"))
        self.user = kwargs.get("user")

class File(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    event_id = db.Column(db.String(35), db.ForeignKey('event.id'))

    def __init__(self, event):
        self.id = generate_id()
        self.event = event

class Audience(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phonenumber = db.Column(db.String(100))
    status = db.Column(db.String(10))
    event_id = db.Column(db.String(35), db.ForeignKey('event.id'))

    def __init__(self, event, audience_info):
        self.id = generate_id()
        self.name = audience_info[0]
        self.email = audience_info[1]
        self.phonenumber = str(audience_info[2])
        self.status = "Pending"
        self.event = event

class Purchase(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    price = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.String(35), db.ForeignKey('user.id'))
    event_id = db.Column(db.String(35), db.ForeignKey('event.id'))
    promo_id = db.Column(db.String(35), db.ForeignKey('promo_code.id'))

class ResetPassword(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    deadline = db.Column(db.DateTime)

class PromoCode(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    discount = db.Column(db.Float(precision=2))
    purchase = db.relationship("Purchase", backref="promo")
