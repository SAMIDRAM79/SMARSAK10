@echo off
echo ============================================
echo SMARTSAK10 - Build Script Windows
echo ============================================
echo.

echo [1/6] Verification des prerequis...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Node.js n'est pas installe!
    echo Telechargez depuis: https://nodejs.org/
    pause
    exit /b 1
)

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Python n'est pas installe!
    echo Telechargez depuis: https://www.python.org/
    pause
    exit /b 1
)

echo OK - Node.js et Python sont installes
echo.

echo [2/6] Installation des dependances Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
cd ..
echo OK - Dependances Backend installees
echo.

echo [3/6] Installation des dependances Frontend...
cd frontend
call yarn install
if %ERRORLEVEL% NEQ 0 (
    echo Installation de Yarn...
    npm install -g yarn
    call yarn install
)
cd ..
echo OK - Dependances Frontend installees
echo.

echo [4/6] Build du Frontend...
cd frontend
call yarn build
cd ..
echo OK - Frontend build
echo.

echo [5/6] Preparation Electron...
if not exist electron-app mkdir electron-app
cd electron-app

if not exist package.json (
    call npm init -y
    call npm install electron electron-builder --save-dev
)

if not exist frontend-build (
    mkdir frontend-build
)
xcopy /E /I /Y ..\frontend\build frontend-build

if not exist backend (
    mkdir backend
)
xcopy /E /I /Y ..\backend backend

if not exist python (
    mkdir python
)
xcopy /E /I /Y ..\backend\venv python

cd ..
echo OK - Electron prepare
echo.

echo [6/6] Build de l'installateur Windows...
cd electron-app
call npm run build:win
cd ..
echo.
echo ============================================
echo BUILD TERMINE !
echo ============================================
echo.
echo L'installateur se trouve dans:
echo electron-app\dist\SMARTSAK10-Setup-1.0.0.exe
echo.
pause
