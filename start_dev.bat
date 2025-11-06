@echo off
setlocal
echo ============================
echo 🚀 DEV: Flask + Vite (2 fenêtres)
echo ============================

start cmd /k "cd /d %~dp0chatbot-mini && if not exist venv (python -m venv venv) && call venv\Scripts\activate && python -m pip install -r requirements.txt && python run_api.py"
start cmd /k "cd /d %~dp0chatbot-frontend && if not exist node_modules (npm ci) && npm run dev"

echo ✅ Flask : http://127.0.0.1:8000
echo ✅ React : http://127.0.0.1:5173
pause
