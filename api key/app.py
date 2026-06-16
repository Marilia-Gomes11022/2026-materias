from flask import Flask, jsonify, request
from functools import wraps
import os

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY", "minha-chave-secreta")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return jsonify({"erro": "API key inválida ou ausente"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/hello", methods=["GET"])
@require_api_key
def hello():
    return jsonify({
        "mensagem": "Hello World"
    })

if __name__ == "__main__":
    app.run(debug=True)
