@echo off
cd /d C:\xampp\htdocs\prospects\storeman-etl
call .venv\Scripts\activate.bat
python pages/Bulk_Import.py
pause


