from flask import Blueprint, jsonify, request

from app.controllers.team_controller import criar_mensagem, listar_mensagens


messages_bp = Blueprint("messages", __name__)


@teams_bp.route("/", methods=["GET"])
def get_teams():
    response, status = listar_times()
    return jsonify(response), status


@teams_bp.route("/", methods=["POST"])
def post_team():
    data = request.get_json()
    response, status = criar_time(data)
    return jsonify(response), status
