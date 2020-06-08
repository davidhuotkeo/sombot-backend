from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(db)

from app.models.database import (
    User,
    Event,
    File,
    Audience,
    Purchase,
    ResetPassword,
    PromoCode
)

from app.models.schema import (
    EventSchema,
    AudienceSchema
)