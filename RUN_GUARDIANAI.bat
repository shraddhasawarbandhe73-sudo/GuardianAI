@echo off
cd /d "%~dp0"
echo GuardianAI setup: creating virtual environment if needed...
if not exist .venv (
  py -m venv .venv
  if errorlevel 1 python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Opening GuardianAI in your browser...
start "" http://127.0.0.1:5000
python app.py
pause
