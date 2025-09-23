from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.bot import ChatBot
import os

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
    return jsonify(status="ok")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
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
