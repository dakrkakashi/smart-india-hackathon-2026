@echo off
title Pralay Early Warning System Launcher
echo ========================================================
echo        Starting Pralay Early Warning System
echo ========================================================

echo [1/3] Ensuring Docker services (PostgreSQL, Redis, Mosquitto) are running...
docker-compose up -d postgres redis mosquitto

echo [2/3] Starting FastAPI Backend on http://localhost:8000...
start "Pralay Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo [3/3] Starting React Frontend on http://localhost:5173...
start "Pralay Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo ========================================================
echo  All services launched!
echo  - Frontend UI:  http://localhost:5173
echo  - Backend API:  http://localhost:8000
echo  - Swagger Docs: http://localhost:8000/docs
echo ========================================================
pause
