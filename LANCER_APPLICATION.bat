@echo off
title SMARTSAK10 - Lanceur Application
color 0A

echo ============================================
echo    SMARTSAK10 - IEPP SAKASSOU
echo    Systeme de Management Scolaire
echo ============================================
echo.

echo [1/3] Verification MongoDB...
net start MongoDB >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo OK - MongoDB demarre
) else (
    echo ATTENTION: MongoDB n'est pas demarre
    echo Tentative de demarrage...
    sc start MongoDB >nul 2>nul
    timeout /t 3 >nul
)
echo.

echo [2/3] Demarrage Backend (FastAPI)...
cd /d "%~dp0backend"
start "SMARTSAK10 Backend" cmd /k "venv\Scripts\activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
echo OK - Backend demarre sur port 8001
echo.

echo [3/3] Demarrage Frontend (React)...
cd /d "%~dp0frontend"
start "SMARTSAK10 Frontend" cmd /k "yarn start"
echo OK - Frontend demarre sur port 3000
echo.

echo ============================================
echo APPLICATION DEMARREE !
echo ============================================
echo.
echo Acces: http://localhost:3000
echo Email: konatdra@gmail.com
echo.
echo Les fenetres Backend et Frontend doivent rester ouvertes.
echo.
echo Appuyez sur une touche pour ouvrir l'application...
pause >nul
start http://localhost:3000
