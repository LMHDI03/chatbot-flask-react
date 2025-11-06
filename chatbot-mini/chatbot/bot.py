# chatbot/bot.py
from .faq import FAQ
import random
import datetime
import re
from typing import Tuple

import requests

from .nlp import tokenize, clean_tokens, extract_name, extract_city
from .intents import load_intents


class ChatBot:
    def __init__(self):
        self.intents = load_intents()
        self.memory = {
            "name": None,
            "default_city": "Rabat",
        }
        self.faq = FAQ() #loading fichier faq
    def handle(self, message: str) -> str:
        raw = (message or "").strip()
        text = raw.lower()
        tokens = clean_tokens(tokenize(text))
    # --------------------------
    # Intents helpers (rule-based)
    # --------------------------
    def _is_greet(self, tokens) -> bool:
        return any(t in tokens for t in ("salut", "bonjour", "coucou", "hey"))

    def _is_goodbye(self, text: str) -> bool:
        t = text.lower()
        return any(k in t for k in ("au revoir", "a plus", "à plus", "bye"))

    def _is_time(self, tokens) -> bool:
        # gère "quelle heure", "il est quelle heure", "donne l'heure"
        return any(t in tokens for t in ("heure", "time"))

    def _is_date(self, tokens) -> bool:
        # gère "quelle date", "on est quel jour", "quel jour"
        return ("date" in tokens) or ("jour" in tokens)

    def _is_ask_name(self, text: str) -> bool:
        t = text.lower()
        # normalisé sans apostrophes : "je mappelle" côté extract_name
        keys = [
            "comment je mappelle",
            "quel est mon nom",
            "tu te souviens de mon nom",
        ]
        return any(k in t for k in keys)

    def _is_weather(self, text: str) -> bool:
        t = text.lower()
        # couvre "meteo", "météo", "quel temps", "temps à ..."
        return any(k in t for k in ("meteo", "météo", "quel temps", "temps"))

    # --------------------------
    # Open-Meteo (gratuit, sans clé)
    # --------------------------
    def _wmo_desc(self, code: int) -> str:
        WMO = {
            0: "ciel dégagé",
            1: "quelques nuages",
            2: "partiellement nuageux",
            3: "couvert",
            45: "brouillard",
            48: "brouillard givrant",
            51: "bruine faible",
            53: "bruine",
            55: "bruine forte",
            61: "pluie faible",
            63: "pluie",
            65: "pluie forte",
            66: "pluie verglaçante faible",
            67: "pluie verglaçante forte",
            71: "neige faible",
            73: "neige",
            75: "neige forte",
            77: "grains de neige",
            80: "averses faibles",
            81: "averses",
            82: "averses fortes",
            95: "orage",
            96: "orage avec grêle faible",
            99: "orage avec grêle forte",
        }
        return WMO.get(code, f"code météo {code}")

    def _geocode_city(self, city: str) -> Tuple[float, float] | None:
        try:
            r = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "fr", "format": "json"},
                timeout=8,
            )
            r.raise_for_status()
            data = r.json()
            if not data.get("results"):
                return None
            res = data["results"][0]
            return float(res["latitude"]), float(res["longitude"])
        except Exception:
            return None

    def _fetch_weather(self, city: str) -> Tuple[str, float] | None:
        try:
            coords = self._geocode_city(city)
            if not coords:
                return None
            lat, lon = coords
            r = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,weather_code",
                    "timezone": "auto",
                    "lang": "fr",
                },
                timeout=8,
            )
            r.raise_for_status()
            data = r.json()
            cur = data.get("current")
            if not cur:
                return None
            temp = float(cur.get("temperature_2m"))
            code = int(cur.get("weather_code"))
            desc = self._wmo_desc(code)
            return desc, temp
        except Exception:
            return None

    # --------------------------
    # Rendering
    # --------------------------
    def _render(self, intent: str, template_list: list[str], extra: dict | None = None) -> str:
        extra = extra or {}
        text = random.choice(template_list)

        # Heure / Date
        if "{time}" in text:
            now = datetime.datetime.now().strftime("%H:%M")
            text = text.replace("{time}", now)
        if "{date}" in text:
            today = datetime.date.today().strftime("%d/%m/%Y")
            text = text.replace("{date}", today)

        # Nom
        if "{name}" in text:
            name = extra.get("name") or self.memory.get("name") or "je ne sais pas encore"
            text = text.replace("{name}", str(name))

        # Météo
        if intent == "weather":
            city = extra.get("city") or self.memory.get("default_city")
            desc = extra.get("weather_desc", "météo indisponible")
            temp = extra.get("temp", "?")
            text = text.replace("{city}", str(city))
            text = text.replace("{weather_desc}", str(desc))
            text = text.replace("{temp}", f"{temp}")

        return text

    # --------------------------
    # Core
    # --------------------------
    def handle(self, message: str) -> str:
        raw = (message or "").strip()
        text = raw.lower()
        tokens = clean_tokens(tokenize(text))

        # 1) mémorisation du prénom
        name = extract_name(raw)
        if name:
            self.memory["name"] = name
            return self._render(
                "set_name",

                self.intents["set_name"]["responses"],
                {"name": name},
            )

        # 2) demande du prénom mémorisé
        if self._is_ask_name(text):
            if self.memory["name"]:
                return self._render("ask_name", self.intents["ask_name"]["responses"])
            return "Je ne connais pas encore ton prénom. Dis-moi « je m'appelle <Prénom> » 😊."

        # 3) heure / date
        if self._is_time(tokens):
            return self._render("time", self.intents["time"]["responses"])
        if self._is_date(tokens):
            return self._render("date", self.intents["date"]["responses"])

        # 4) météo
        if self._is_weather(text):
            city = extract_city(raw) or self.memory.get("default_city") or "Rabat"
            meta = {}
            w = self._fetch_weather(city)
            if w:
                desc, temp = w
                meta = {"city": city, "weather_desc": desc, "temp": temp}
            else:
                meta = {"city": city, "weather_desc": "météo indisponible", "temp": "?"}
            return self._render("weather", self.intents["weather"]["responses"], meta)

        # 5) salutations / au revoir
        if self._is_greet(tokens):
            return self._render("greet", self.intents["greet"]["responses"])
        if self._is_goodbye(text):
            return self._render("goodbye", self.intents["goodbye"]["responses"])
       
        ans = self.faq.find_answer(raw)
        if ans:
            return ans
        # 6) fallback
        return self._render("fallback", self.intents["fallback"]["responses"])


# -------------------------------------------------------
# Mode debug (permet de tester sans passer par l'API Flask)
# Lance:  python -m chatbot.bot
# -------------------------------------------------------
if __name__ == "__main__":
    bot = ChatBot()
    print("Bot debug 👇 (tape ENTER pour quitter)\n")
    while True:
        try:
            msg = input("Vous: ")
        except (EOFError, KeyboardInterrupt):
            break
        if not msg:
            break
        print("Bot:", bot.handle(msg))
