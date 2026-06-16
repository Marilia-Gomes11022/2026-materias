from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
import os

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY", "chave_secreta")

def require_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"erro": "Token ausente"}), 401
        token = auth_header.split(" ")[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["POST"])
def login():
    token = jwt.encode(
        {"user": "exemplo", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"token": token})

@app.route("/hello", methods=["GET"])
@require_jwt
def hello():
    return jsonify({
        "mensagem": "Hello World"
    })

if __name__ == "__main__":
    app.run(debug=True)
