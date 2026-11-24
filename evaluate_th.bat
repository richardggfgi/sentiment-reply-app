@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
rem Finds the project folder and the review file by itself, runs evaluate.py, saves results to eval_result_th.txt
set "D=%~dp0"
if exist "%D%app.py" goto found
if exist "%D%sentiment-reply-app\app.py" set "D=%D%sentiment-reply-app\" & goto found
if exist "%D%sentiment-reply-app\sentiment-reply-app\app.py" set "D=%D%sentiment-reply-app\sentiment-reply-app\" & goto found
echo Could not find app.py near this file.
pause
exit /b 1
:found
cd /d "%D%"
if not exist ".venv\Scripts\python.exe" (
  echo Run run.bat once first, then try again.
  pause
  exit /b 1
)

set "F="
if exist "%D%restaurant_reviews_150_th.tsv" set "F=%D%restaurant_reviews_150_th.tsv"
if not defined F if exist "%USERPROFILE%\Downloads\restaurant_reviews_150_th.tsv" set "F=%USERPROFILE%\Downloads\restaurant_reviews_150_th.tsv"
if not defined F (
  echo Could not find restaurant_reviews_150_th.tsv in the project folder or Downloads.
  pause
  exit /b 1
)

echo Testing with: %F%
echo This takes a few minutes (150 Thai reviews)...
echo.
".venv\Scripts\python.exe" evaluate.py "%F%" > eval_result_th.txt 2>&1
type eval_result_th.txt
echo.
echo Saved to: %CD%\eval_result_th.txt
pause
