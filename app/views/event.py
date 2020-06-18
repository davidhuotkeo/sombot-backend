from flask import Blueprint, jsonify, request, abort
from app.models import (
    PromoCode,
    Event,
    EventSchema,
    Audience,
    AudienceSchema,
    Purchase,
    User
)
from app.controllers.database_controllers import add_to_database
from app.controllers.file_controller import csv_control
# from app.controllers.email import (AudienceEmail, send_email)
from threading import Thread
from app import basic_auth

event = Blueprint("event", __name__)

@event.route("/event/create/<userid>", methods=["POST"])
def create_event(userid):
    event_data = request.json
    if not event_data:
        abort(403)
    
    # query user if not found return None
    user = User.query.filter(User.id == userid).first()
    if not user:
        return jsonify({"event": None}), 404

    # submit to database
    new_event = Event(event_data, user=user)
    add_to_database(new_event)

    return jsonify({"event": new_event.user_id})

@event.route("/events/<userid>", methods=["GET"])
def get_events(userid):
    user = User.query.filter(User.id == userid).first()
    event = user.event
    schema = EventSchema(many=True)
    events = schema.dump(event)
    return jsonify(events)

@event.route("/event/audience/<eventid>", methods=["GET"])
def audience(eventid):
    # query all the audiences in the event
    # if not response 404 not found
    audiences = Audience.query.filter(Audience.event_id == eventid).all()
    if not audiences:
        abort(404)
    
    # get the query to the dictionary using marshmallow
    schema = AudienceSchema(many=True)
    audience_data = schema.dump(audiences)

    return jsonify(audience_data)

@event.route("/event/upload/<eventid>", methods=["POST"])
def upload_file(eventid):
    # Get the request file
    data = request.files
    if not data:
        abort(403)

    print(eventid)
    # check if there is a event
    event_availability = Event.query.filter(Event.id == eventid).first()
    if not event_availability:
        return jsonify({"uploaded": False}), 404

    # Get file and upload to database
    file = data.get('file')
    row = csv_control(file, event_id=eventid)
    return jsonify({"uploaded": True})

# @event.route("/event/send/<eventid>")
# def send_ticket(eventid):
#     # Query event
#     event = Event.query.filter(Event.id == eventid).first()

#     # get the audience relationship
#     audiences = event.audience

#     # if there is no audience uploaded response 404
#     if not audiences:
#         return jsonify({"sent": None}), 404

#     # create the list and some variables for send_email func kwargs
#     audience_list_object = []
#     subject = f"Ticket from {event.name} Event"
#     msg = event.body

#     # load the Audience object and append to the list
#     for people in audiences:
#         identity = people.id
#         email = people.email
#         audience_list_object.append(AudienceEmail(identity, email))
    
#     # Parallelism sending email
#     email_arguments = {"audiences": audience_list_object, "subject": subject, "message": msg}
#     email_parallel = Thread(target=send_email, kwargs=email_arguments)

#     # Strart parallelism
#     email_parallel.start()

#     return jsonify({"sent": True})

@event.route("/promocode", methods=["GET"])
def promocode():
    # query promocode
    # if found return discounted
    promocode = request.json.get("code")
    code = PromoCode.query.filter(PromoCode.id == promocode).first()

    if code:
        return jsonify({'discount': code.discount})
    return jsonify({'discount': None})
