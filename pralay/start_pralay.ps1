# Pralay Early Warning System Launcher for PowerShell
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "       Starting Pralay Early Warning System" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$root = $PSScriptRoot

Write-Host "`n[1/3] Ensuring Docker infrastructure is running..." -ForegroundColor Yellow
docker-compose -f "$root\docker-compose.yml" up -d postgres redis mosquitto

Write-Host "`n[2/3] Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Yellow
Start-Process cmd.exe -ArgumentList "/k cd /d `"$root\backend`" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

Write-Host "`n[3/3] Starting React Frontend on http://localhost:5173..." -ForegroundColor Yellow
Start-Process cmd.exe -ArgumentList "/k cd /d `"$root\frontend`" && npm run dev"

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " All services launched in independent windows!" -ForegroundColor Green
Write-Host " - Frontend UI:  http://localhost:5173" -ForegroundColor White
Write-Host " - Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host " - Swagger Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Green
