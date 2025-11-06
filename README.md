# 🤖 Mini Chatbot – Interface Web

Une interface web moderne et légère pour discuter avec une API de chatbot locale ou distante.  
Ce projet est développé avec **React + TypeScript**, et communique avec une API (par exemple : Flask) via le point d’accès `/chat`.

---

## 🌟 Fonctionnalités

- 💬 Interface simple, responsive et fluide  
- 🌓 Mode **clair / sombre** persistant  
- 💾 Sauvegarde automatique de la conversation (localStorage)  
- 📤 Export des discussions en `.txt` ou `.json`  
- 🧠 Suggestions de requêtes intelligentes  
- ⚙️ URL d’API configurable directement dans l’interface  
- 🧹 Effacement rapide de la conversation  
- 📋 Copie rapide d’un message par clic  

---

## 🧰 Technologies utilisées

| Catégorie | Outils |
|------------|--------|
| **Frontend** | React + TypeScript |
| **Styling** | CSS pur (`app.css`) |
| **Build Tool** | Vite |
| **Backend attendu** | API REST (`/chat`) – ex : Flask |
| **Langages** | JavaScript, TypeScript, Python |

---

## 🚀 Installation et lancement

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/<votre-nom-utilisateur>/<nom-du-repo>.git
cd <nom-du-repo>
2️⃣ Installer les dépendances frontend
bash
Copier le code
npm install
3️⃣ (Optionnel) Créer et activer un environnement virtuel Python
Si tu utilises un backend Flask :

bash
Copier le code
python -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate   # Linux / macOS
4️⃣ Installer les dépendances backend
bash
Copier le code
pip install -r requirements.txt
5️⃣ Lancer le serveur React (frontend)
bash
Copier le code
npm run dev
Le projet sera accessible sur :

arduino
Copier le code
http://localhost:5173/
6️⃣ Lancer le serveur Flask (backend)
bash
Copier le code
python run_api.py
L’API doit répondre sur :

arduino
Copier le code
http://127.0.0.1:8000/chat
⚙️ Structure du projet
bash
Copier le code
📦 chatbot-project
 ┣ 📂 chatbot-frontend
 ┃ ┣ 📂 src
 ┃ ┃ ┣ 📜 ChatbotUI.tsx      → Composant principal React
 ┃ ┃ ┣ 📜 app.css            → Styles globaux + dark mode
 ┃ ┃ ┗ 📜 main.tsx           → Point d’entrée React
 ┃ ┣ 📜 index.html
 ┃ ┣ 📜 package.json
 ┣ 📂 chatbot-mini
 ┃ ┣ 📜 run_api.py           → Serveur Flask + routes API
 ┃ ┣ 📜 bot.py               → Logique du chatbot
 ┣ 📜 deploy_all.py          → Script d’automatisation du build
 ┣ 📜 README.md              → Documentation du projet
🧩 Déploiement
▶️ Script deploy_all.py
Ce script automatise le processus :

Supprime les fichiers temporaires et anciens builds

Exécute npm run build

Copie le contenu du dossier dist/ dans le backend Flask (chatbot-mini/web)

Exécution :
bash
Copier le code
python deploy_all.py
🪄 Exécution manuelle :
bash
Copier le code
npm run build
Puis copier le contenu de dist/ dans le dossier où Flask sert les fichiers statiques (chatbot-mini/web).

💡 Améliorations futures
🔌 Indicateur visuel de connexion API (en ligne / hors ligne)

🗣️ Ajout de la synthèse vocale (text-to-speech)

⌨️ Support de commandes vocales

🧠 Ajout d’un mode GPT local ou API OpenAI

🌐 Internationalisation (i18n)

💅 Effets visuels modernes (animations, transitions CSS)

📱 Refonte responsive mobile améliorée

👨‍💻 Auteur
El Mehdi REGRAGUI
🎓 Master 2 – Systèmes Intelligents & Mobiles
📍 Taza, Maroc
📧 Contact : [mehdiregragui00@gmail.com]
🔗 LinkedIn https://www.linkedin.com/in/mehdi-regragui200
