@echo off
echo ========================================
echo   SMARTSAK10 - BUILD WINDOWS
echo ========================================
echo.

echo [1/5] Verification des prerequis...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Telecharger: https://www.python.org/downloads/
    pause
    exit /b 1
)

where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Node.js n'est pas installe ou pas dans le PATH
    echo Telecharger: https://nodejs.org/
    pause
    exit /b 1
)

where yarn >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Yarn n'est pas installe
    echo Installer: npm install -g yarn
    pause
    exit /b 1
)

echo Tous les prerequis sont installes!
echo.

echo [2/5] Installation des dependances backend...
cd ..\backend
pip install -q -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR lors de l'installation des dependances backend
    pause
    exit /b 1
)
echo Backend OK!
echo.

echo [3/5] Installation des dependances frontend...
cd ..\frontend
call yarn install --silent
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR lors de l'installation des dependances frontend
    pause
    exit /b 1
)
echo Frontend OK!
echo.

echo [4/5] Installation des dependances Electron...
cd ..\electron-app
call yarn install --silent
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR lors de l'installation des dependances Electron
    pause
    exit /b 1
)
echo Electron OK!
echo.

echo [5/5] Construction de l'executable Windows...
echo Ceci peut prendre 5-10 minutes...
echo.
call yarn dist:win

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   BUILD TERMINE AVEC SUCCES!
    echo ========================================
    echo.
    echo Le fichier d'installation est disponible dans:
    echo %CD%\dist\SMARTSAK10 Setup 1.0.0.exe
    echo.
    echo Version portable dans:
    echo %CD%\dist\win-unpacked\SMARTSAK10.exe
    echo.
) else (
    echo.
    echo ========================================
    echo   ERREUR LORS DU BUILD
    echo ========================================
    echo.
    echo Verifiez les messages d'erreur ci-dessus
    echo.
)

pause
