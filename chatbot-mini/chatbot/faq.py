# chatbot/faq.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, List, Dict
from .nlp import normalize, tokenize

FAQ_PATH = Path(__file__).resolve().parent.parent / "data" / "faq.json"

class FAQ:
    def __init__(self):
        with open(FAQ_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.entries: List[Dict] = data.get("entries", [])

    def find_answer(self, user_text: str, min_score: int = 2) -> Optional[str]:
        """
        Retourne la réponse si un pattern a assez de mots en commun (score).
        min_score=2 évite les faux positifs.
        """
        user_tokens = set(tokenize(normalize(user_text)))
        best = ("", 0)
        for entry in self.entries:
            for pat in entry.get("patterns", []):
                pat_tokens = set(tokenize(normalize(pat)))
                score = len(user_tokens & pat_tokens)
                if score > best[1]:
                    best = (entry.get("answer", ""), score)
        return best[0] if best[1] >= min_score and best[0] else None
