@echo off
REM run_test.bat — script pentru testare (Windows)
REM Schimbă directorul la calea proiectului și încearcă să ruleze punctele posibile de intrare Python

cd /d "D:\Proiecte\IA\Transcriere"
echo Current directory: %cd%

REM Verifică dacă există Python în PATH
python --version >nul 2>&1
if ERRORLEVEL 1 (
  echo Python nu a fost găsit in PATH. Asigură-te că Python este instalat si adaugat la PATH.
  pause
  exit /b 1
)

REM Încearcă puncte de intrare cunoscute din repo (prioritate pentru minutes_generator)
if exist "minutes_generator.py" (
  echo Rularea minutes_generator.py...
  python minutes_generator.py %*
  exit /b %ERRORLEVEL%
)

if exist "pipeline.py" (
  echo Rularea pipeline.py...
  python pipeline.py %*
  exit /b %ERRORLEVEL%
)

if exist "transcriber.py" (
  echo Rularea transcriber.py...
  python transcriber.py %*
  exit /b %ERRORLEVEL%
)

REM Alte entrypoint-uri posibile
if exist "main.py" (
  echo Rularea main.py...
  python main.py %*
  exit /b %ERRORLEVEL%
)

if exist "src\main.py" (
  echo Rularea src\main.py...
  python src\main.py %*
  exit /b %ERRORLEVEL%
)

if exist "app.py" (
  echo Rularea app.py...
  python app.py %*
  exit /b %ERRORLEVEL%
)

echo Nu s-a gasit un punct de intrare cunoscut (minutes_generator.py, pipeline.py, transcriber.py, main.py, src\main.py, app.py).
echo Editeaza run_test.bat daca proiectul tau are alt entrypoint sau ruleaza manual comanda dorita.
pause
exit /b 2
