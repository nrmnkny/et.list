@echo off
cd /d C:\xampp\htdocs\prospects\storeman-etl
call .venv\Scripts\activate.bat
python bulk_fetch_trends.py
pause


