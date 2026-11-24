@echo off
chcp 65001 >nul
rem Finds the project folder by itself, then uses Python 3.12 (x64) in its own venv,
rem because Python 3.15 ARM64 has no prebuilt wheels for pyarrow/cryptography yet.
set "D=%~dp0"
if exist "%D%app.py" goto found
if exist "%D%sentiment-reply-app\app.py" set "D=%D%sentiment-reply-app\" & goto found
if exist "%D%sentiment-reply-app\sentiment-reply-app\app.py" set "D=%D%sentiment-reply-app\sentiment-reply-app\" & goto found
echo Could not find app.py near this file. Put run.bat in the same folder as app.py.
pause
exit /b 1
:found
cd /d "%D%"
echo Project folder: %CD%

if exist ".venv\Scripts\python.exe" goto venv_ok
echo === Installing Python 3.12 x64 (if it asks, type y and press Enter) ===
py install 3.12-64
echo === Creating environment ===
py -V:3.12-64 -m venv .venv
if errorlevel 1 (
  echo.
  echo *** Could not create environment with Python 3.12-64. Screenshot this window and send it to Claude. ***
  pause
  exit /b 1
)
:venv_ok

echo === Installing packages (first time takes a few minutes) ===
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo *** Install failed. Take a screenshot of this window and send it to Claude. ***
  pause
  exit /b 1
)

rem Stop Streamlit from asking for an email on first run
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
  mkdir "%USERPROFILE%\.streamlit" 2>nul
  (echo [general]& echo email = "") > "%USERPROFILE%\.streamlit\credentials.toml"
)

echo.
echo === Starting app (browser will open) ===
".venv\Scripts\python.exe" -m streamlit run app.py
pause
