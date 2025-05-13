import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Variables de entorno necesarias
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
GITHUB_FILE = os.getenv("GITHUB_FILE")  # Debe ser 'sync/strovo-tv.m3u'

# Ruta principal para servir la lista M3U
@app.route("/strovo-tv.m3u")
def get_m3u():
    if not all([GITHUB_TOKEN, GITHUB_USER, GITHUB_REPO, GITHUB_FILE]):
        return "Error: Variables de entorno no configuradas correctamente.", 500

    api_url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE}?ref={GITHUB_BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        raw_url = json_data.get("download_url")

        if raw_url:
            raw_file = requests.get(raw_url)
            return Response(
                raw_file.text,
                mimetype="audio/x-mpegurl",
                headers={
                    "Content-Disposition": "inline; filename=strovo-tv.m3u",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        else:
            return "Error: No se encontró el archivo de descarga.", 500
    else:
        return f"Error: Código {response.status_code} al acceder al archivo.", 500

# Ruta de prueba para verificar funcionamiento en Heroku
@app.route("/ping")
def ping():
    return "Funciona en Heroku"

# Inicia la aplicación en el puerto asignado por Heroku
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

