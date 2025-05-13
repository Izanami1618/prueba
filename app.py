import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Variables de entorno para GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
GITHUB_FILE = os.getenv("GITHUB_FILE")

@app.route("/")
def get_m3u():
    if not all([GITHUB_TOKEN, GITHUB_USER, GITHUB_REPO, GITHUB_FILE]):
        return "Error: Variables de entorno de GitHub no están configuradas.", 500

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}?ref={GITHUB_BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        file_content = json_data.get("download_url")

        if file_content:
            raw_file = requests.get(file_content)
            return Response(raw_file.text, mimetype="audio/x-mpegurl")
        else:
            return "Error: No se pudo obtener el enlace de descarga.", 500
    else:
        return f"Error: No se pudo acceder al archivo. Código {response.status_code}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
