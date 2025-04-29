@echo off
cd /d "%~dp0"

REM Create venv if it doesn't exist
if not exist ".venv\Scripts\activate" (
    python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate

REM Install requirements
pip install --upgrade pip
pip install -r requirements.txt

REM Run the tool
python hotkey_copy_test.py 