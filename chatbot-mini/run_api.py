<<<<<<< HEAD
from flask import Flask, request, jsonify, send_from_directory
=======
from flask import Flask, request, jsonify
>>>>>>> origin/main
from flask_cors import CORS
from chatbot.bot import ChatBot
import os

<<<<<<< HEAD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONT_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONT_DIR, static_url_path="/")
CORS(app)

bot = ChatBot()

@app.get("/health")
def health():
=======
app = Flask(__name__, static_folder="frontend", static_url_path="")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # désactive le cache des fichiers statiques (dev)
CORS(app)
bot = ChatBot()

# Désactive le cache surtout pour index.html
@app.after_request
def add_no_cache_headers(resp):
    if resp.mimetype == "text/html":
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
    return resp

@app.get("/health")
def health():
    print("GET /health")
>>>>>>> origin/main
    return jsonify(status="ok")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
<<<<<<< HEAD
    text = data.get("message", "")
    if not isinstance(text, str) or not text.strip():
        return jsonify(error="Field 'message' (string) is required."), 400
    reply = bot.handle(text)
    return jsonify(reply=reply)

# Sert index.html du build React
@app.get("/")
def index():
    return send_from_directory(FRONT_DIR, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
=======
    print("POST /chat payload:", repr(data))
    text = data.get("message", "")
    if not isinstance(text, str) or not text.strip():
        return jsonify(error="Field 'message' (string) is required."), 400
    return jsonify(reply=bot.handle(text))

@app.get("/")
def home():
    print("GET / (index)")
    return app.send_static_file("index.html")

# essaie de servir un fichier statique, sinon renvoie index.html (SPA)
@app.get("/<path:subpath>")
def spa(subpath):
    try:
        return app.send_static_file(subpath)
    except Exception:
        return app.send_static_file("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
>>>>>>> origin/main
