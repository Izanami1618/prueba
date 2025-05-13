import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Variables de entorno necesarias
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
GITHUB_FILE = os.getenv("GITHUB_FILE")

@app.route("/lista.m3u")
def get_m3u():
    # Verifica que las variables estén definidas
    if not all([GITHUB_TOKEN, GITHUB_USER, GITHUB_REPO, GITHUB_FILE]):
        return "Error: Variables de entorno de GitHub no están configuradas correctamente.", 500

    # URL para acceder al archivo en el repositorio
    api_url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{GITHUB_FILE}?ref={GITHUB_BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Solicita la metadata del archivo
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        raw_url = json_data.get("download_url")

        if raw_url:
            # Descarga el archivo directamente desde GitHub raw
            raw_file = requests.get(raw_url)

            return Response(
                raw_file.text,
                mimetype="audio/x-mpegurl",
                headers={
                    "Content-Disposition": "inline; filename=lista.m3u",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        else:
            return "Error: No se pudo obtener el enlace de descarga del archivo.", 500
    else:
        return f"Error: No se pudo acceder al archivo en GitHub. Código {response.status_code}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
