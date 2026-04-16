from app.extensions import db
from app.models.participant import Participant
from app.schemas.participant_schema import ParticipantSchema
from app.utils.response import success_response


participant_schema = ParticipantSchema()
participants_schema = ParticipantSchema(many=True)


def listar_participantes():
    participantes = Participant.query.all()
    return success_response(participants_schema.dump(participantes))


def criar_participante(data):
    dados_validados = participant_schema.load(data)

    novo_participante = Participant(**dados_validados)

    db.session.add(novo_participante)
    db.session.commit()

    return success_response(participant_schema.dump(novo_participante), 201)


def atualizar_participante(id, data):
    participante = Participant.query.get_or_404(id)

    dados_validados = user_schema.load(data, partial=True)

    for campo, valor in dados_validados.items():
        setattr(participante, campo, valor)

    db.session.commit()

    return success_response(user_schema.dump(participante))


def deletar_participante(id):
    participante = Participant.query.get_or_404(id)

    db.session.delete(participante)
    db.session.commit()

    return "", 204
