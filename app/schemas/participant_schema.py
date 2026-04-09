from marshmallow import fields, validate

from app.extensions import ma
from app.models.participant import Participant


class ParticipantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Participant

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(required=True)
    idade = ma.auto_field(required=True)
    team_id = ma.auto_field(dump_only=True)
