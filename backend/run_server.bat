@echo off
cd /d C:\Users\user\Desktop\CowID\backend
set PYTHONPATH=C:\Users\user\Desktop\CowID\backend
"C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
