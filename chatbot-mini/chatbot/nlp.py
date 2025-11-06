import re

STOPWORDS = {"je", "tu", "il", "elle", "et", "de", "le", "la", "les", "un", "une", "a", "à"}

def normalize(text: str) -> str:
    return text.lower().strip()

def tokenize(text: str):
    text = normalize(text)
    return re.findall(r"\b\w+\b", text, flags=re.UNICODE)

def clean_tokens(tokens):
    return [t for t in tokens if t not in STOPWORDS]

import re

def extract_name(text: str) -> str | None:
    """
    Reconnaît :
    - "je m'appelle Mehdi"
    - "je mappelle Mehdi" (sans apostrophe)
    - "mon nom est Mehdi"
    """
    t = text.lower().strip()

    # enlève l’apostrophe pour harmoniser
    t = t.replace("'", "")

    m = re.search(r"je mappelle\s+([a-zA-ZÀ-ÖØ-öø-ÿ\-]+)", t)
    if not m:
        m = re.search(r"mon nom est\s+([a-zA-ZÀ-ÖØ-öø-ÿ\-]+)", t)
    if m:
        return m.group(1).capitalize()
    return None


def extract_city(text: str) -> str | None:
    """
    Heuristiques simples :
    - "météo rabat", "meteo fes"
    - "météo à casablanca", "quel temps à tanger"
    - sinon None
    """
    t = normalize(text)
    # "meteo rabat" / "météo rabat"
    m = re.search(r"(?:meteo|météo)\s+([a-zA-ZÀ-ÖØ-öø-ÿ\-]+)", t)
    if not m:
        # "... à rabat"
        m = re.search(r"(?:meteo|météo|temps|meteo a|météo à|quel temps à|quel temps a).*\s(?:a|à)\s([a-zA-ZÀ-ÖØ-öø-ÿ\-]+)", t)
    if m:
        city = m.group(1).strip()
        return city.capitalize()
    return None
