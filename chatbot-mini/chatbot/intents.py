import json
from pathlib import Path

INTENTS_PATH = Path(__file__).resolve().parent.parent / "data" / "intents.json"

def load_intents():
    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
