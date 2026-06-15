@echo off
cd /d D:\WarToWin
call venv\Scripts\activate
start cmd /k python manage.py runserver 127.0.0.1:8000
timeout /t 3
start cmd /k D:\cloudflared\cloudflared.exe tunnel --config D:\cloudflared\config.yml run wartowin