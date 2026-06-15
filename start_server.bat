@echo off

echo ==========================
echo DEMARRAGE DJANGO
echo ==========================

cd /d D:\WarToWin

call venv\Scripts\activate

start "Django" cmd /k "waitress-serve --host=127.0.0.1 --port=8000 wartowin.wsgi:application"

timeout /t 5 /nobreak > nul

echo ==========================
echo DEMARRAGE CLOUDFLARE
echo ==========================

start "Cloudflare" cmd /k "D:\cloudflared\cloudflared.exe tunnel --url http://127.0.0.1:8000"

pause