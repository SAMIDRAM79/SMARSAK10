# 📦 GUIDE D'INSTALLATION SMARTSAK10 SOUS WINDOWS

## 🎯 Vue d'ensemble

SMARTSAK10 est une application de gestion scolaire qui peut fonctionner :
- **En ligne** : via navigateur web
- **Hors ligne** : comme application de bureau Windows (.exe)

---

## 📋 Prérequis

### Pour l'installation de base :
- Windows 10 ou supérieur (64-bit)
- 4 GB RAM minimum
- 2 GB espace disque

### Pour le développement/packaging :
- Node.js 16+ ([télécharger](https://nodejs.org/))
- Python 3.9+ ([télécharger](https://www.python.org/))
- MongoDB Community Edition ([télécharger](https://www.mongodb.com/try/download/community))

---

## 🚀 MÉTHODE 1 : Installation Application de Bureau (Recommandée)

### Étape 1 : Télécharger l'application packagée

1. Téléchargez `SMARTSAK10-Setup.exe` depuis votre source de distribution
2. Double-cliquez sur le fichier pour lancer l'installation
3. Suivez l'assistant d'installation

### Étape 2 : Installer MongoDB Local (pour utilisation hors ligne)

#### Option A : Installation automatique avec script

1. Ouvrez le dossier d'installation de SMARTSAK10
2. Double-cliquez sur `installer_mongodb.bat`
3. Attendez la fin de l'installation

#### Option B : Installation manuelle

1. **Télécharger MongoDB :**
   - Allez sur https://www.mongodb.com/try/download/community
   - Sélectionnez : Windows / MSI / Latest Version
   - Téléchargez et installez

2. **Configurer MongoDB :**
   ```batch
   # Créer les dossiers de données
   mkdir C:\data\db
   mkdir C:\data\log
   
   # Ajouter MongoDB au PATH (optionnel)
   setx PATH "%PATH%;C:\Program Files\MongoDB\Server\7.0\bin"
   ```

3. **Démarrer MongoDB :**
   - Ouvrez `services.msc`
   - Cherchez "MongoDB"
   - Clic droit → Démarrer
   
   OU via commande :
   ```batch
   net start MongoDB
   ```

### Étape 3 : Lancer SMARTSAK10

1. Double-cliquez sur l'icône SMARTSAK10 sur le bureau
2. Ou cherchez "SMARTSAK10" dans le menu Démarrer
3. L'application se lance automatiquement

### Étape 4 : Première utilisation

1. **Connexion :**
   - Email : `konatdra@gmail.com`
   - (Pas de mot de passe requis)

2. **Configuration initiale :**
   - Allez dans **Paramètres**
   - Vérifiez/modifiez :
     - Année scolaire actuelle
     - DRENA, IEPP, Région

3. **Import des données :**
   - Allez dans **Import Données**
   - Importez le fichier Excel AGCEPE
   - Importez les photos des élèves (fichier ZIP)

---

## 🛠️ MÉTHODE 2 : Créer votre propre package Windows

### Prérequis techniques

```batch
# Installer Node.js et Python
winget install -e --id OpenJS.NodeJS
winget install -e --id Python.Python.3.11

# Installer Yarn globalement
npm install -g yarn
```

### Étape 1 : Préparer le projet

1. **Télécharger le code source** (depuis votre dépôt)

2. **Installer les dépendances Backend :**
   ```batch
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Installer les dépendances Frontend :**
   ```batch
   cd frontend
   yarn install
   ```

### Étape 2 : Configuration Electron

1. **Créer le dossier Electron :**
   ```batch
   mkdir electron-app
   cd electron-app
   ```

2. **Initialiser le projet Electron :**
   ```batch
   npm init -y
   npm install electron electron-builder
   ```

3. **Créer `main.js` :** (voir fichier ci-dessous)

4. **Créer `package.json` pour Electron :** (voir fichier ci-dessous)

### Étape 3 : Build de l'application

1. **Build Frontend :**
   ```batch
   cd frontend
   yarn build
   ```

2. **Copier les fichiers nécessaires :**
   ```batch
   # Copier le build frontend
   xcopy /E /I frontend\build electron-app\frontend-build
   
   # Copier le backend
   xcopy /E /I backend electron-app\backend
   
   # Copier Python
   xcopy /E /I venv electron-app\python
   ```

3. **Build Electron :**
   ```batch
   cd electron-app
   npm run build:win
   ```

4. **L'installateur sera créé dans :**
   ```
   electron-app/dist/SMARTSAK10-Setup-1.0.0.exe
   ```

---

## 📱 MÉTHODE 3 : Utilisation via Navigateur (Mode Web)

### Configuration requise

- MongoDB installé et démarré
- Node.js installé
- Python installé

### Étape 1 : Démarrer MongoDB

```batch
net start MongoDB
```

### Étape 2 : Démarrer le Backend

```batch
cd backend
venv\Scripts\activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Étape 3 : Démarrer le Frontend

```batch
cd frontend
yarn start
```

### Étape 4 : Accéder à l'application

Ouvrez votre navigateur : `http://localhost:3000`

---

## 🔧 Configuration Avancée

### Variables d'environnement

#### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=smartscool
CORS_ORIGINS=*
AUTHORIZED_EMAIL=konatdra@gmail.com
```

#### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_USER_EMAIL=konatdra@gmail.com
```

### Ports utilisés

- **Backend API** : 8001
- **Frontend Web** : 3000
- **MongoDB** : 27017

---

## 🎨 Fonctionnalités de l'application

### Modules disponibles :

1. **Paramètres** - Configuration générale
2. **Import Données** - Import Excel AGCEPE + Photos
3. **Répartition CEPE** - Gestion centres d'examen
4. **Cartes Scolaires** - Génération cartes (4 modèles vifs)
5. **Gestion Élèves** - Base de données élèves
6. **Notes & Bulletins** - Saisie et génération
7. **Statistiques** - Résultats par école/secteur/commune

---

## 🐛 Résolution des problèmes

### L'application ne démarre pas

1. **Vérifier MongoDB :**
   ```batch
   net start MongoDB
   ```

2. **Vérifier les ports :**
   ```batch
   netstat -ano | findstr "8001 3000 27017"
   ```

3. **Logs de l'application :**
   - Vérifiez `C:\Users\[Votre_Nom]\AppData\Roaming\SMARTSAK10\logs`

### Erreur "Cannot connect to database"

1. MongoDB n'est pas démarré :
   ```batch
   net start MongoDB
   ```

2. Vérifier la connexion :
   ```batch
   mongo
   # Si ça fonctionne, MongoDB est OK
   ```

### Erreur "Port already in use"

1. **Trouver le processus utilisant le port :**
   ```batch
   netstat -ano | findstr ":8001"
   ```

2. **Arrêter le processus :**
   ```batch
   taskkill /PID [PID_NUMBER] /F
   ```

### L'application est lente

1. Vérifier l'espace disque disponible (min 2GB)
2. Vérifier la RAM disponible (min 4GB)
3. Redémarrer l'application
4. Redémarrer MongoDB

---

## 📞 Support

Pour toute question ou problème :
- Email : konatdra@gmail.com
- Documentation : Consultez les fichiers dans le dossier d'installation

---

## 🔄 Mises à jour

### Mise à jour automatique

L'application vérifie automatiquement les mises à jour au démarrage.

### Mise à jour manuelle

1. Téléchargez la nouvelle version
2. Désinstallez l'ancienne version (vos données sont conservées)
3. Installez la nouvelle version

---

## 💾 Sauvegarde des données

### Sauvegarde automatique

Les données sont sauvegardées dans :
```
C:\data\db\smartscool
```

### Sauvegarde manuelle

```batch
mongodump --db smartscool --out C:\Backup\smartscool_%date%
```

### Restauration

```batch
mongorestore --db smartscool C:\Backup\smartscool_[DATE]
```

---

## ✅ Checklist post-installation

- [ ] MongoDB installé et démarré
- [ ] SMARTSAK10 installé
- [ ] Connexion réussie avec konatdra@gmail.com
- [ ] Paramètres configurés (année scolaire, DRENA, IEPP)
- [ ] Données Excel importées
- [ ] Photos importées
- [ ] Test de génération de cartes scolaires
- [ ] Test de répartition CEPE

---

## 📄 Licence et Crédits

**SMARTSAK10** - Système de Management Scolaire

Développé pour : IEPP SAKASSOU  
Version : 1.0.0  
Année : 2024-2025

© Tous droits réservés
