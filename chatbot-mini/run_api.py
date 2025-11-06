from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatbot.bot import ChatBot
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONT_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONT_DIR, static_url_path="/")
CORS(app)

bot = ChatBot()

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
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
