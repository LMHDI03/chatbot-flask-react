# 🤖 Chatbot Flask + React

Un mini-projet complet combinant **Flask (Python)** et **React (TypeScript)** pour créer un chatbot simple mais extensible.  
Il inclut une API backend en Flask et une interface utilisateur moderne en React avec persistance locale.

---

## ✨ Fonctionnalités

- **Chat en temps réel** avec réponses basiques (FAQ + météo via OpenWeather API).
- **Backend Flask** exposant une API REST (`/chat`, `/health`).
- **Frontend React** avec interface type "messagerie" :
  - Bulles utilisateur (bleu, à droite) et bot (gris, à gauche).
  - Timestamps automatiques.
  - Suggestions cliquables.
  - Bouton copier 📋.
- **Options avancées** :
  - Thème clair 🌞 / sombre 🌙 (persistant dans `localStorage`).
  - Historique des conversations sauvegardé dans `localStorage`.
  - Personnalisation de l’URL API.
  - Export de conversation en `.txt` et `.json`.
  - Bouton pour effacer la discussion.

---

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/ton-compte/chatbot-flask-react.git
cd chatbot-flask-react


2. Backend (Flask)

Aller dans le dossier chatbot-mini :

cd chatbot-mini
pip install flask flask-cors requests
python run_api.py


Le serveur tourne sur :
👉 http://127.0.0.1:8000

3. Frontend (React + Vite)

Aller dans le dossier chatbot-frontend :

cd chatbot-frontend
npm install
npm run build


Déployer vers le backend (copie du dossier dist/ dans chatbot-mini/frontend/) :

python deploy_all.py


Puis relancer le backend Flask.
Le front est alors accessible via :
👉 http://127.0.0.1:8000

📂 Structure du projet
chatbot-project/
├── chatbot-mini/         # Backend Flask
│   ├── bot.py            # Logique du bot
│   ├── run_api.py        # API Flask
│   └── frontend/         # Build du frontend React (copié après build)
└── chatbot-frontend/     # Frontend React (Vite + TS + CSS)
    ├── src/
    │   ├── ChatbotUI.tsx # Composant principal
    │   ├── app.css       # Styles custom
    │   └── main.tsx
    └── package.json

🚀 Améliorations futures

Connexion avec un modèle NLP avancé (spaCy, Hugging Face, OpenAI API…).

Gestion multi-utilisateurs avec base de données.

Ajout d’un logo, favicon et page d’accueil stylisée.

Déploiement sur Heroku, Vercel ou Render.

👤 Auteur

Projet développé par Mehdi (Master SIM).
👉 Exemple de mini-projet académique pour enrichir le CV avec un stack Python + React.