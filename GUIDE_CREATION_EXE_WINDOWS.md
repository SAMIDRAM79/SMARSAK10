# 🔧 GUIDE COMPLET : CRÉER LE FICHIER .EXE POUR WINDOWS

## 📋 Vue d'ensemble

Ce guide vous explique comment transformer votre application SMARTSAK10 en un fichier `.exe` installable sur n'importe quel PC Windows.

---

## ⚙️ PRÉREQUIS (à installer sur votre PC de développement)

### 1. Node.js (obligatoire)
```
Télécharger : https://nodejs.org/
Version recommandée : 18.x ou 20.x LTS
```

**Vérification :**
```cmd
node --version
npm --version
```

### 2. Python (obligatoire)
```
Télécharger : https://www.python.org/downloads/
Version recommandée : 3.9 ou supérieure
```

**Vérification :**
```cmd
python --version
pip --version
```

### 3. MongoDB (obligatoire pour le package)
```
Télécharger : https://www.mongodb.com/try/download/community
Version : 7.0 ou supérieure
```

---

## 📦 MÉTHODE 1 : Build Automatique (Recommandée)

### Étape 1 : Préparer le projet

1. **Télécharger le code source complet**
   - Depuis votre dépôt Git ou Emergent
   - Extraire dans `C:\SMARTSAK10`

2. **Vérifier la structure :**
   ```
   C:\SMARTSAK10\
   ├── backend\
   ├── frontend\
   ├── electron-app\
   ├── BUILD_INSTRUCTIONS_WINDOWS.bat
   └── GUIDE_INSTALLATION_WINDOWS.md
   ```

### Étape 2 : Exécuter le script de build

1. **Ouvrir le dossier dans l'explorateur**
   ```
   C:\SMARTSAK10
   ```

2. **Double-cliquer sur :**
   ```
   BUILD_INSTRUCTIONS_WINDOWS.bat
   ```

3. **Le script va automatiquement :**
   - ✅ Vérifier Node.js et Python
   - ✅ Installer les dépendances Backend
   - ✅ Installer les dépendances Frontend
   - ✅ Compiler le Frontend
   - ✅ Préparer Electron
   - ✅ Créer l'installateur .exe

4. **Attendre la fin (10-15 minutes)**

### Étape 3 : Récupérer le fichier .exe

Le fichier sera créé dans :
```
C:\SMARTSAK10\electron-app\dist\SMARTSAK10-Setup-1.0.0.exe
```

**Taille approximative :** 200-300 MB

---

## 🛠️ MÉTHODE 2 : Build Manuel (Détaillé)

### Étape 1 : Installer les outils de développement

```cmd
# Installer Yarn globalement
npm install -g yarn

# Installer Electron Builder
npm install -g electron-builder
```

### Étape 2 : Préparer le Backend

```cmd
cd C:\SMARTSAK10\backend

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Créer un exécutable Python portable (optionnel)
pip install pyinstaller
```

### Étape 3 : Compiler le Frontend

```cmd
cd C:\SMARTSAK10\frontend

# Installer les dépendances
yarn install

# Build production
yarn build
```

**Résultat :** Dossier `frontend\build` créé

### Étape 4 : Configurer Electron

1. **Créer le dossier electron-app**
   ```cmd
   cd C:\SMARTSAK10
   mkdir electron-app
   cd electron-app
   ```

2. **Initialiser le projet**
   ```cmd
   npm init -y
   ```

3. **Installer Electron et Builder**
   ```cmd
   npm install electron@27.0.0 --save-dev
   npm install electron-builder@24.6.4 --save-dev
   ```

4. **Copier les fichiers nécessaires**

   **Copier main.js** (déjà créé dans `/app/electron-app/main.js`)
   
   **Copier package.json** (déjà créé dans `/app/electron-app/package.json`)

5. **Copier le frontend compilé**
   ```cmd
   mkdir frontend-build
   xcopy /E /I /Y ..\frontend\build frontend-build
   ```

6. **Copier le backend**
   ```cmd
   mkdir backend
   xcopy /E /I /Y ..\backend backend
   ```

7. **Copier Python**
   ```cmd
   mkdir python
   xcopy /E /I /Y ..\backend\venv python
   ```

8. **Copier le logo**
   ```cmd
   copy ..\frontend\public\logo-iepp.jpg logo.jpg
   ```

### Étape 5 : Build l'application

```cmd
# Dans C:\SMARTSAK10\electron-app
npm run build:win
```

**Attendre 10-15 minutes...**

### Étape 6 : Récupérer l'installateur

```
C:\SMARTSAK10\electron-app\dist\SMARTSAK10-Setup-1.0.0.exe
```

---

## 🎨 PERSONNALISATION

### Changer l'icône de l'application

1. **Créer une icône .ico**
   - Utiliser un convertisseur en ligne : https://convertio.co/fr/png-ico/
   - Taille recommandée : 256x256 pixels

2. **Remplacer dans `electron-app/package.json` :**
   ```json
   "build": {
     "win": {
       "icon": "chemin/vers/votre-icone.ico"
     }
   }
   ```

### Changer le nom de l'application

Dans `electron-app/package.json` :
```json
{
  "name": "smartsak10",
  "version": "1.0.0",
  "build": {
    "appId": "com.iepp.smartsak10",
    "productName": "SMARTSAK10"
  }
}
```

### Changer le nom de l'installateur

Dans `electron-app/package.json` :
```json
"build": {
  "nsis": {
    "artifactName": "SMARTSAK10-Installer-${version}.${ext}"
  }
}
```

---

## 📝 FICHIER package.json COMPLET pour Electron

Créer `electron-app/package.json` :

```json
{
  "name": "smartsak10",
  "version": "1.0.0",
  "description": "Système de Management Scolaire - IEPP SAKASSOU",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build:win": "electron-builder --win --x64",
    "build:win32": "electron-builder --win --ia32"
  },
  "build": {
    "appId": "com.iepp.smartsak10",
    "productName": "SMARTSAK10",
    "copyright": "Copyright © 2024 IEPP SAKASSOU",
    "win": {
      "target": ["nsis"],
      "icon": "logo.jpg",
      "requestedExecutionLevel": "requireAdministrator"
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true,
      "allowElevation": true,
      "createDesktopShortcut": true,
      "createStartMenuShortcut": true,
      "shortcutName": "SMARTSAK10",
      "installerIcon": "logo.jpg",
      "uninstallerIcon": "logo.jpg",
      "installerHeader": "logo.jpg",
      "installerHeaderIcon": "logo.jpg",
      "language": "1036"
    },
    "files": [
      "main.js",
      "package.json",
      "frontend-build/**/*",
      "backend/**/*",
      "python/**/*",
      "logo.jpg"
    ],
    "extraFiles": [
      {
        "from": "backend",
        "to": "resources/backend",
        "filter": ["**/*"]
      },
      {
        "from": "python",
        "to": "resources/python",
        "filter": ["**/*"]
      }
    ],
    "directories": {
      "output": "dist",
      "buildResources": "."
    }
  },
  "keywords": [
    "education",
    "school",
    "management",
    "cepe",
    "iepp",
    "sakassou"
  ],
  "author": "IEPP SAKASSOU",
  "license": "PROPRIETARY",
  "devDependencies": {
    "electron": "^27.0.0",
    "electron-builder": "^24.6.4"
  }
}
```

---

## 🔧 RÉSOLUTION DES PROBLÈMES

### Problème 1 : "node n'est pas reconnu"

**Solution :**
```cmd
# Ajouter Node.js au PATH
setx PATH "%PATH%;C:\Program Files\nodejs"

# Redémarrer le terminal
```

### Problème 2 : "python n'est pas reconnu"

**Solution :**
```cmd
# Réinstaller Python avec l'option "Add to PATH" cochée
# Ou ajouter manuellement :
setx PATH "%PATH%;C:\Users\VotreNom\AppData\Local\Programs\Python\Python311"
```

### Problème 3 : "electron-builder échoue"

**Solution :**
```cmd
# Nettoyer le cache
npm cache clean --force
rd /s /q node_modules
del package-lock.json

# Réinstaller
npm install
```

### Problème 4 : "Out of memory" pendant le build

**Solution :**
```cmd
# Augmenter la mémoire Node.js
set NODE_OPTIONS=--max-old-space-size=4096
npm run build:win
```

### Problème 5 : Le .exe est trop gros (>500MB)

**Solutions :**
1. Exclure les fichiers inutiles dans `package.json` :
   ```json
   "files": [
     "!**/*.map",
     "!**/test/**",
     "!**/__pycache__/**"
   ]
   ```

2. Compresser avec 7-Zip après build

### Problème 6 : L'application ne démarre pas après installation

**Vérifications :**
1. MongoDB est installé sur le PC cible
2. Les permissions administrateur sont accordées
3. Vérifier les logs dans `%APPDATA%\SMARTSAK10\logs`

---

## 📦 DISTRIBUER LE FICHIER .EXE

### Option 1 : USB / Disque externe
```
1. Copier SMARTSAK10-Setup-1.0.0.exe sur la clé USB
2. Copier aussi INSTALLER_MONGODB_WINDOWS.bat
3. Distribuer aux utilisateurs
```

### Option 2 : Cloud (Google Drive, OneDrive)
```
1. Uploader le fichier .exe
2. Partager le lien
3. Les utilisateurs téléchargent et installent
```

### Option 3 : Serveur Web
```
1. Héberger sur votre serveur
2. URL : https://votresite.com/downloads/SMARTSAK10-Setup.exe
3. Créer une page de téléchargement
```

---

## ✅ CHECKLIST AVANT DISTRIBUTION

Avant de distribuer le .exe, vérifiez :

- [ ] Le fichier .exe s'installe correctement
- [ ] L'application se lance après installation
- [ ] MongoDB est inclus ou documenté séparément
- [ ] Le guide utilisateur est fourni (GUIDE_INSTALLATION_WINDOWS.md)
- [ ] L'icône de l'application est correcte
- [ ] Le nom de l'application est correct
- [ ] Les raccourcis bureau/menu démarrer fonctionnent
- [ ] La désinstallation fonctionne
- [ ] Testé sur Windows 10 et 11
- [ ] Testé avec et sans droits administrateur

---

## 🚀 COMMANDES RAPIDES

```cmd
# Build complet en une commande
cd C:\SMARTSAK10 && BUILD_INSTRUCTIONS_WINDOWS.bat

# Build uniquement Electron
cd electron-app && npm run build:win

# Test local avant build
cd electron-app && npm start

# Nettoyer et rebuild
rd /s /q electron-app\dist && npm run build:win
```

---

## 📊 TAILLE DES FICHIERS

**Estimations :**
- Frontend build : ~10 MB
- Backend + Python : ~150 MB
- Electron framework : ~100 MB
- MongoDB (séparé) : ~200 MB

**Total installateur .exe : ~250-300 MB**

---

## 🎓 TUTORIEL VIDÉO (étapes clés)

1. ✅ Installer Node.js, Python
2. ✅ Télécharger le code source
3. ✅ Double-clic sur BUILD_INSTRUCTIONS_WINDOWS.bat
4. ✅ Attendre la fin
5. ✅ Récupérer le .exe dans electron-app\dist
6. ✅ Tester l'installation
7. ✅ Distribuer

---

## 📞 SUPPORT

En cas de problème :
- Email : konatdra@gmail.com
- Consultez : GUIDE_INSTALLATION_WINDOWS.md
- Vérifiez les logs dans : %APPDATA%\SMARTSAK10

---

## 🔄 MISES À JOUR

Pour créer une nouvelle version :

1. Modifier le numéro de version dans `electron-app/package.json` :
   ```json
   "version": "1.1.0"
   ```

2. Rebuild :
   ```cmd
   npm run build:win
   ```

3. Le nouveau fichier sera :
   ```
   SMARTSAK10-Setup-1.1.0.exe
   ```

---

✅ **VOTRE FICHIER .EXE EST PRÊT À ÊTRE DISTRIBUÉ !**

📦 Emplacement final : `electron-app\dist\SMARTSAK10-Setup-1.0.0.exe`
