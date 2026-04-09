from app.extensions import db
from app.models.team import Team
from app.models.participant import Participant
from app.schemas.team_schema import TeamSchema
from app.utils.response import success_response


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)


def listar_mensagens():
    mensagens = Message.query.all()
    return success_response(messages_schema.dump(mensagens))


def listar_mensagens_por_usuario(user_id):
    user = User.query.get_or_404(user_id)
    mensagens = user.messages
    return success_response(messages_schema.dump(mensagens))


def criar_equipe(data):
    dados_validados = team_schema.load(data)

    Participant.query.get_or_404(dados_validados["team_id"])

    nova_mensagem = Team(**dados_validados)

    db.session.add(nova_mensagem)
    db.session.commit()

    return success_response(team_schema.dump(nova_mensagem), 201)

