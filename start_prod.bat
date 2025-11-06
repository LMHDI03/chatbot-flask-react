@echo off
setlocal
cd /d %~dp0
python deploy_all.py || goto :end
start cmd /k "cd /d %~dp0chatbot-mini && if not exist venv (python -m venv venv) && call venv\Scripts\activate && python -m pip install -r requirements.txt && python run_api.py"
echo ✅ Ouvre: http://127.0.0.1:8000
:end
pause
