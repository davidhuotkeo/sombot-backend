from app.models import ma
from app.models.database import (
    Event,
    Audience,
)

class EventSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "date", "user_id")

class AudienceSchema(ma.Schema):
    class Meta:
        fields = ("name", "email", "status")
