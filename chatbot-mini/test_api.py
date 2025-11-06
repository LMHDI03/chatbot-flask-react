# test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def post_chat(message: str):
    r = requests.post(f"{BASE_URL}/chat", json={"message": message}, timeout=10)
    r.raise_for_status()
    return r.json()["reply"]

def main():
    # 1) ping
    h = requests.get(f"{BASE_URL}/health", timeout=5)
    print("Health:", h.json())

    # 2) tests simples
    print(">> salut")
    print("Bot:", post_chat("salut"))

    print(">> quelle heure")
    print("Bot:", post_chat("quelle heure"))

    print(">> on est quel jour")
    print("Bot:", post_chat("on est quel jour"))

    print(">> je m'appelle Mehdi")
    print("Bot:", post_chat("je m'appelle Mehdi"))

    print(">> tu te souviens de mon nom ?")
    print("Bot:", post_chat("tu te souviens de mon nom"))

    print(">> météo Rabat")
    print("Bot:", post_chat("météo Rabat"))

    # 3) fallback
    print(">> blablabla phrase inconnue")
    print("Bot:", post_chat("blablabla phrase inconnue"))

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l’API. Lance d’abord:  python run_api.py")
    except requests.HTTPError as e:
        print("❌ Erreur HTTP:", e.response.status_code, e.response.text)
    except Exception as e:
        print("❌ Erreur:", e)
