from flask import Flask, jsonify, request
import base64

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "senha123"

def check_auth(authorization_header):
    if not authorization_header or not authorization_header.startswith("Basic "):
        return False

    credentials = base64.b64decode(authorization_header[6:]).decode("utf-8")
    username, password = credentials.split(":", 1)

    return username == USERNAME and password == PASSWORD

def unauthorized():
    return jsonify({"erro": "Acesso não autorizado"}), 401, {
        "WWW-Authenticate": 'Basic realm="Login necessário"'
    }

@app.route("/hello", methods=["GET"])
def hello():
    if not check_auth(request.headers.get("Authorization")):
        return unauthorized()

    return jsonify({"mensagem": "Hello World"})

if __name__ == "__main__":
    app.run(debug=True)
