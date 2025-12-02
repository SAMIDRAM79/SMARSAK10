# ============================================
# SMARTSAK10 - Script Build Complet (PowerShell)
# Crée un fichier .exe installable pour Windows
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SMARTSAK10 - Build Application Windows" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$ProjectRoot = $PSScriptRoot
$BackendDir = Join-Path $ProjectRoot "backend"
$FrontendDir = Join-Path $ProjectRoot "frontend"
$ElectronDir = Join-Path $ProjectRoot "electron-app"
$DistDir = Join-Path $ElectronDir "dist"

# Fonction pour vérifier un programme
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

# Fonction pour afficher une étape
function Write-Step {
    param($Number, $Total, $Message)
    Write-Host ""
    Write-Host "[$Number/$Total] $Message" -ForegroundColor Yellow
    Write-Host ("=" * 60) -ForegroundColor Gray
}

# ÉTAPE 1 : Vérification des prérequis
Write-Step 1 8 "Vérification des prérequis"

$Prerequisites = @{
    "node" = "Node.js"
    "npm" = "NPM"
    "python" = "Python"
    "pip" = "Pip"
}

$AllPrerequisitesMet = $true

foreach ($cmd in $Prerequisites.Keys) {
    if (Test-Command $cmd) {
        $version = & $cmd --version 2>&1
        Write-Host "✓ $($Prerequisites[$cmd]) trouvé: $version" -ForegroundColor Green
    } else {
        Write-Host "✗ $($Prerequisites[$cmd]) NON TROUVÉ!" -ForegroundColor Red
        $AllPrerequisitesMet = $false
    }
}

if (-not $AllPrerequisitesMet) {
    Write-Host ""
    Write-Host "ERREUR: Certains prérequis manquent!" -ForegroundColor Red
    Write-Host "Veuillez installer:" -ForegroundColor Yellow
    Write-Host "  - Node.js: https://nodejs.org/" -ForegroundColor White
    Write-Host "  - Python: https://www.python.org/" -ForegroundColor White
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host ""
Write-Host "✓ Tous les prérequis sont satisfaits!" -ForegroundColor Green

# ÉTAPE 2 : Installation Yarn
Write-Step 2 8 "Vérification de Yarn"

if (-not (Test-Command "yarn")) {
    Write-Host "Installation de Yarn..." -ForegroundColor Yellow
    npm install -g yarn
} else {
    Write-Host "✓ Yarn déjà installé" -ForegroundColor Green
}

# ÉTAPE 3 : Backend - Environnement virtuel et dépendances
Write-Step 3 8 "Configuration du Backend Python"

Push-Location $BackendDir

Write-Host "Création de l'environnement virtuel Python..." -ForegroundColor Cyan
if (-not (Test-Path "venv")) {
    python -m venv venv
}

Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Cyan
& "$BackendDir\venv\Scripts\Activate.ps1"

Write-Host "Installation des dépendances Backend..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

Write-Host "✓ Backend configuré" -ForegroundColor Green
Pop-Location

# ÉTAPE 4 : Frontend - Installation des dépendances
Write-Step 4 8 "Installation des dépendances Frontend"

Push-Location $FrontendDir

Write-Host "Installation avec Yarn..." -ForegroundColor Cyan
yarn install

Write-Host "✓ Dépendances Frontend installées" -ForegroundColor Green
Pop-Location

# ÉTAPE 5 : Build du Frontend
Write-Step 5 8 "Compilation du Frontend React"

Push-Location $FrontendDir

Write-Host "Build production..." -ForegroundColor Cyan
yarn build

if (Test-Path "build") {
    Write-Host "✓ Frontend compilé avec succès" -ForegroundColor Green
} else {
    Write-Host "✗ Erreur lors de la compilation du Frontend!" -ForegroundColor Red
    Pop-Location
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Pop-Location

# ÉTAPE 6 : Préparation Electron
Write-Step 6 8 "Préparation de l'application Electron"

# Créer le dossier electron-app s'il n'existe pas
if (-not (Test-Path $ElectronDir)) {
    New-Item -ItemType Directory -Path $ElectronDir | Out-Null
}

Push-Location $ElectronDir

# Initialiser npm si nécessaire
if (-not (Test-Path "package.json")) {
    Write-Host "Initialisation du projet Electron..." -ForegroundColor Cyan
    npm init -y
}

# Installer Electron et Builder
Write-Host "Installation d'Electron et Electron Builder..." -ForegroundColor Cyan
npm install electron@27.0.0 electron-builder@24.6.4 --save-dev

# Copier les fichiers nécessaires
Write-Host "Copie du Frontend compilé..." -ForegroundColor Cyan
if (Test-Path "frontend-build") {
    Remove-Item -Recurse -Force "frontend-build"
}
Copy-Item -Recurse -Force (Join-Path $FrontendDir "build") "frontend-build"

Write-Host "Copie du Backend..." -ForegroundColor Cyan
if (Test-Path "backend") {
    Remove-Item -Recurse -Force "backend"
}
Copy-Item -Recurse -Force $BackendDir "backend"

Write-Host "Copie de l'environnement Python..." -ForegroundColor Cyan
if (Test-Path "python") {
    Remove-Item -Recurse -Force "python"
}
Copy-Item -Recurse -Force (Join-Path $BackendDir "venv") "python"

# Copier le logo
Write-Host "Copie du logo..." -ForegroundColor Cyan
$LogoSource = Join-Path $FrontendDir "public\logo-iepp.jpg"
if (Test-Path $LogoSource) {
    Copy-Item -Force $LogoSource "logo.jpg"
} else {
    Write-Host "  ATTENTION: Logo non trouvé, utilisation du logo par défaut" -ForegroundColor Yellow
}

Write-Host "✓ Electron préparé" -ForegroundColor Green
Pop-Location

# ÉTAPE 7 : Build de l'application
Write-Step 7 8 "Compilation de l'application Windows"

Push-Location $ElectronDir

Write-Host "Lancement du build Electron (cela peut prendre 10-15 minutes)..." -ForegroundColor Cyan
Write-Host "Veuillez patienter..." -ForegroundColor Yellow
Write-Host ""

npm run build:win

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Build terminé avec succès!" -ForegroundColor Green
} else {
    Write-Host "✗ Erreur lors du build!" -ForegroundColor Red
    Pop-Location
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Pop-Location

# ÉTAPE 8 : Vérification et affichage du résultat
Write-Step 8 8 "Vérification du fichier .exe"

$ExeFiles = Get-ChildItem -Path $DistDir -Filter "*.exe" -ErrorAction SilentlyContinue

if ($ExeFiles) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "   BUILD TERMINÉ AVEC SUCCÈS !" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Fichier(s) créé(s):" -ForegroundColor Cyan
    
    foreach ($file in $ExeFiles) {
        $size = [math]::Round($file.Length / 1MB, 2)
        Write-Host "  📦 $($file.Name)" -ForegroundColor White
        Write-Host "     Taille: $size MB" -ForegroundColor Gray
        Write-Host "     Emplacement: $($file.FullName)" -ForegroundColor Gray
        Write-Host ""
    }
    
    Write-Host "PROCHAINES ÉTAPES:" -ForegroundColor Yellow
    Write-Host "  1. Testez l'installation sur un PC propre" -ForegroundColor White
    Write-Host "  2. Assurez-vous que MongoDB est installé sur le PC cible" -ForegroundColor White
    Write-Host "  3. Distribuez le fichier .exe aux utilisateurs" -ForegroundColor White
    Write-Host ""
    Write-Host "Pour installer MongoDB, utilisez:" -ForegroundColor Cyan
    Write-Host "  INSTALLER_MONGODB_WINDOWS.bat" -ForegroundColor White
    Write-Host ""
    
    # Proposer d'ouvrir le dossier
    $openFolder = Read-Host "Voulez-vous ouvrir le dossier de distribution? (O/N)"
    if ($openFolder -eq "O" -or $openFolder -eq "o") {
        explorer.exe $DistDir
    }
    
} else {
    Write-Host ""
    Write-Host "✗ Aucun fichier .exe trouvé dans le dossier dist!" -ForegroundColor Red
    Write-Host "Vérifiez les erreurs ci-dessus." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Script terminé" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Read-Host "Appuyez sur Entrée pour quitter"
