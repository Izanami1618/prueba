import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Configurar variables de entorno para autenticación en Bitbucket
BITBUCKET_TOKEN = os.getenv("BITBUCKET_TOKEN")
BITBUCKET_REPO = "strovo-tv/amaterasu"  # Reemplaza con tu usuario/repositorio
BRANCH_NAME = "IZANAGI"  # Tu rama en Bitbucket
FILE_PATH = "strovo"  # Nombre del archivo M3U dentro del repo

@app.route("/")
def get_m3u():
    url = f"https://bitbucket.org/{BITBUCKET_REPO}/raw/{BRANCH_NAME}/{FILE_PATH}?access_token={BITBUCKET_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        return Response(response.text, mimetype="audio/x-mpegurl")
    else:
        return f"Error: No se pudo obtener el archivo. Código {response.status_code}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
