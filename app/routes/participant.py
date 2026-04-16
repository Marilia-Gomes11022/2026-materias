from flask import Blueprint, jsonify, request

from app.controllers.team_controller import listar_mensagens_por_participante
from app.controllers.participant_controller import (
    atualizar_participante,
    criar_participante,
    deletar_participante,
    listar_participante,
)


participants_bp = Blueprint("participants", __name__)


@participants_bp.route("/", methods=["GET"])
def get_participants():
    response, status = listar_participantes()
    return jsonify(response), status


@participants_bp.route("/", methods=["POST"])
def post_participant():
    data = request.get_json()
    response, status = criar_participante(data)
    return jsonify(response), status


@participants_bp.route("/<int:id>", methods=["PATCH"])
def patch_participant(id):
    data = request.get_json()
    response, status = atualizar_participante(id, data)
    return jsonify(response), status


@participants_bp.route("/<int:id>", methods=["DELETE"])
def delete_participant(id):
    response, status = deletar_participante(id)
    if status == 204:
        return "", 204
    return jsonify(response), status


@participants_bp.route("/<int:participant_id>/teams", methods=["GET"])
def get_participant_teams(participant_id):
    response, status = listar_times_por_participante(participant_id)
    return jsonify(response), status
