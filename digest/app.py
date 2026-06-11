from flask import Flask, jsonify, request
import hashlib
import uuid
import time

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "senha123"
REALM = "minha-api"

# Nonce
nonces = {}
NONCE_TTL = 300  # 5 minutos

def gerar_nonce():
    nonce = uuid.uuid4().hex
    nonces[nonce] = time.time()
    return nonce

def nonce_valido(nonce):
    ts = nonces.get(nonce)
    if not ts:
        return False
    if time.time() - ts > NONCE_TTL:
        del nonces[nonce]
        return False
    return True

def md5(texto):
    return hashlib.md5(texto.encode()).hexdigest()

def verificar_digest(header, method):
    if not header or not header.startswith("Digest "):
        return False

    partes = {}
    for parte in header[7:].split(","):
        chave, _, valor = parte.strip().partition("=")
        partes[chave.strip()] = valor.strip().strip('"')

    nonce   = partes.get("nonce", "")
    uri     = partes.get("uri", "")
    nc      = partes.get("nc", "")
    cnonce  = partes.get("cnonce", "")
    qop     = partes.get("qop", "")
    resposta = partes.get("response", "")

    if partes.get("username") != USERNAME or partes.get("realm") != REALM:
        return False
    if not nonce_valido(nonce):
        return False

    ha1 = md5(f"{USERNAME}:{REALM}:{PASSWORD}")
    ha2 = md5(f"{method}:{uri}")

    if qop == "auth":
        esperado = md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}")
    else:
        esperado = md5(f"{ha1}:{nonce}:{ha2}")

    return resposta == esperado

def unauthorized(stale=False):
    nonce = gerar_nonce()
    stale_str = ', stale="true"' if stale else ""
    header = (
        f'Digest realm="{REALM}", '
        f'qop="auth", '
        f'nonce="{nonce}", '
        f'algorithm="MD5"'
        f'{stale_str}'
    )
    return jsonify({"erro": "Acesso não autorizado"}), 401, {
        "WWW-Authenticate": header
    }

@app.route("/hello", methods=["GET"])
def hello():
    if not verificar_digest(request.headers.get("Authorization"), request.method):
        return unauthorized()
    return jsonify({"mensagem": "Hello World"})

if __name__ == "__main__":
    app.run(debug=True)

