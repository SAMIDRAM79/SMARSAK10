@echo off
echo ============================================
echo Installation MongoDB pour SMARTSAK10
echo ============================================
echo.

echo Verification de MongoDB...
where mongod >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo MongoDB est deja installe !
    echo Demarrage du service...
    net start MongoDB
    pause
    exit /b 0
)

echo MongoDB n'est pas installe.
echo.
echo ETAPES D'INSTALLATION:
echo.
echo 1. Telechargement MongoDB Community Edition
echo    URL: https://www.mongodb.com/try/download/community
echo.
echo 2. Selectionnez:
echo    - Platform: Windows
echo    - Package: MSI
echo    - Version: 7.0 (ou superieure)
echo.
echo 3. Installez avec les options par defaut
echo.
echo 4. Creation des dossiers de donnees
mkdir C:\data\db 2>nul
mkdir C:\data\log 2>nul
echo    Dossiers crees: C:\data\db et C:\data\log
echo.
echo 5. Relancez ce script apres l'installation
echo.
echo Appuyez sur une touche pour ouvrir la page de telechargement...
pause >nul
start https://www.mongodb.com/try/download/community
echo.
echo Apres l'installation, relancez ce script !
pause
