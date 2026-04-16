from app.extensions import db
from app.models.team import Team
from app.models.participant import Participant
from app.schemas.team_schema import TeamSchema
from app.utils.response import success_response


team_schema = TeamSchema()
team_schema = TeamSchema(many=True)


def listar_equipe():
    team = Team.query.all()
    return success_response(team_schema.dump(team))


def listar_equipes_por_usuario(user_id):
    participant = Participant.query.get_or_404(participant_id)
    team = participant.team
    return success_response(team_schema.dump(team))


def criar_equipe(data):
    dados_validados = team_schema.load(data)

    Participant.query.get_or_404(dados_validados["team_id"])

    nova_equipe = Team(**dados_validados)

    db.session.add(nova_equipe)
    db.session.commit()

    return success_response(team_schema.dump(nova_equipe), 201)

