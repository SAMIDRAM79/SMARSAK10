# 🖥️ SMARTSAK10 - Installation sur PC Windows

## Guide complet pour installer SMARTSAK10 comme application de bureau

---

## 🎯 Ce que vous allez obtenir

Une application Windows complète avec :
- ✅ Icône sur le bureau
- ✅ Installation via assistant Windows standard
- ✅ Lance l'application en double-cliquant
- ✅ Toutes les fonctionnalités de gestion scolaire
- ✅ Fonctionne offline (avec base de données locale)

---

## 📋 OPTION 1 : Utiliser le fichier .exe déjà construit (SI DISPONIBLE)

### Pour l'utilisateur final :

1. **Télécharger le fichier d'installation**
   - Fichier : `SMARTSAK10 Setup 1.0.0.exe`
   - Emplacement : `/app/electron-app/dist/`

2. **Installer l'application**
   - Double-cliquer sur le fichier .exe
   - Suivre l'assistant d'installation
   - Choisir le dossier d'installation (par défaut : `C:\Program Files\SMARTSAK10`)
   - Cocher "Créer un raccourci sur le bureau"
   - Cliquer sur "Installer"

3. **Lancer l'application**
   - Double-cliquer sur l'icône SMARTSAK10 sur le bureau
   - Ou chercher "SMARTSAK10" dans le menu Démarrer
   - Attendre 30-60 secondes au premier lancement
   - L'application s'ouvre automatiquement dans une fenêtre

4. **Se connecter**
   - L'application s'ouvrira directement (pas de login nécessaire)
   - Email configuré : konatdra@gmail.com

---

## 🔨 OPTION 2 : Construire le fichier .exe vous-même

### Prérequis sur votre PC Windows :

1. **Python 3.11+**
   ```bash
   # Télécharger depuis : https://www.python.org/downloads/
   # Pendant l'installation, COCHER "Add Python to PATH"
   # Vérifier :
   python --version
   ```

2. **Node.js 16+**
   ```bash
   # Télécharger depuis : https://nodejs.org/
   # Installer la version LTS
   # Vérifier :
   node --version
   npm --version
   ```

3. **Yarn**
   ```bash
   npm install -g yarn
   yarn --version
   ```

4. **MongoDB** (optionnel si vous utilisez MongoDB Atlas)
   ```bash
   # Télécharger depuis : https://www.mongodb.com/try/download/community
   # Installer MongoDB Community Edition
   ```

### Étapes de construction :

#### 1. Préparer le projet

```bash
# Ouvrir PowerShell ou CMD
# Naviguer vers le dossier du projet
cd C:\chemin\vers\app

# Installer les dépendances backend
cd backend
pip install -r requirements.txt

# Installer les dépendances frontend
cd ../frontend
yarn install

# Installer les dépendances Electron
cd ../electron-app
yarn install
```

#### 2. Construire l'application

```bash
# Depuis /app/electron-app
yarn dist:win

# Attendre 5-10 minutes...
# Le build va :
# - Empaqueter le backend Python
# - Empaqueter le frontend React
# - Créer l'exécutable Electron
# - Générer l'installateur NSIS
```

#### 3. Récupérer les fichiers

Après le build, vous trouverez dans `/app/electron-app/dist/` :

- **SMARTSAK10 Setup 1.0.0.exe** (~150-200 MB)
  → Installateur Windows standard
  → À distribuer aux utilisateurs

- **Dossier win-unpacked/** (~300-400 MB)
  → Version portable sans installation
  → Contient SMARTSAK10.exe à lancer directement

---

## 🚀 OPTION 3 : Lancer en mode développement (PLUS RAPIDE POUR TESTER)

### Sans construire le .exe :

```bash
# Depuis /app/electron-app
yarn start

# L'application s'ouvrira en mode développement
# Parfait pour tester rapidement
```

---

## 📁 Structure de l'application installée

```
C:\Program Files\SMARTSAK10\
├── SMARTSAK10.exe          # L'application principale
├── resources/
│   ├── backend/            # API FastAPI
│   └── frontend/           # Interface React
└── locales/                # Fichiers de langue
```

---

## ⚙️ Configuration

### Changer la base de données

Par défaut : MongoDB local (`mongodb://localhost:27017`)

Pour utiliser MongoDB Atlas ou une autre base :

1. Ouvrir : `C:\Program Files\SMARTSAK10\resources\backend\.env`
2. Modifier :
   ```
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/smartscool?retryWrites=true&w=majority
   DB_NAME=smartscool
   ```
3. Redémarrer l'application

### Changer l'email administrateur

Par défaut : `konatdra@gmail.com`

1. Ouvrir : `C:\Program Files\SMARTSAK10\resources\backend\.env`
2. Modifier :
   ```
   AUTHORIZED_EMAIL=votreemail@example.com
   ```
3. Redémarrer l'application

---

## 🐛 Dépannage

### Problème : L'application ne démarre pas

**Solutions :**
1. Vérifier que Python est installé : `python --version`
2. Vérifier que Node.js est installé : `node --version`
3. Vérifier que MongoDB est démarré (si base locale)
4. Regarder les logs : `%APPDATA%\smartsak10\logs\`
5. Redémarrer le PC et réessayer

### Problème : "Port already in use"

**Solutions :**
1. Une autre application utilise les ports 8001 ou 3000
2. Fermer les applications qui pourraient utiliser ces ports
3. Ou modifier les ports dans `main.js` :
   ```javascript
   const BACKEND_PORT = 8002;  // Au lieu de 8001
   const FRONTEND_PORT = 3001; // Au lieu de 3000
   ```

### Problème : "Cannot connect to MongoDB"

**Solutions :**
1. Si MongoDB local :
   - Vérifier que MongoDB est installé
   - Démarrer MongoDB : `net start MongoDB`
   - Ou télécharger : https://www.mongodb.com/try/download/community

2. Si MongoDB Atlas :
   - Vérifier la connexion Internet
   - Vérifier les credentials dans `.env`
   - Vérifier que votre IP est autorisée dans Atlas

### Problème : Page blanche au démarrage

**Solutions :**
1. Attendre 60 secondes (compilation au premier lancement)
2. Appuyer sur F5 pour actualiser
3. Vérifier les logs dans la console (F12 si en mode dev)

---

## 📦 Distribution de l'application

### Pour donner l'application à d'autres utilisateurs :

1. **Partager le fichier Setup :**
   - Fichier : `SMARTSAK10 Setup 1.0.0.exe`
   - Taille : ~150-200 MB
   - Envoyer par email, USB, ou serveur de fichiers

2. **Instructions utilisateur :**
   ```
   1. Double-cliquer sur "SMARTSAK10 Setup 1.0.0.exe"
   2. Suivre l'assistant d'installation
   3. Lancer "SMARTSAK10" depuis le bureau
   4. Attendre 30-60 secondes au premier lancement
   5. L'application s'ouvre automatiquement !
   ```

3. **Prérequis utilisateur :**
   - Windows 7 ou supérieur (64-bit recommandé)
   - 4 GB RAM minimum
   - 1 GB d'espace disque
   - (Optionnel) MongoDB si base locale

---

## ✅ Vérification de l'installation

Une fois installé, vérifier que :

- ✅ L'icône est sur le bureau
- ✅ L'application est dans le menu Démarrer
- ✅ Double-clic lance l'application
- ✅ Le dashboard s'affiche avec les statistiques
- ✅ Toutes les pages sont accessibles (Élèves, Classes, Notes, etc.)

---

## 📞 Support

**Email** : konatdra@gmail.com

**En cas de problème, fournir :**
- Version de Windows
- Message d'erreur exact
- Logs de l'application (%APPDATA%\smartsak10\logs\)
- Capture d'écran si possible

---

## 🎉 Félicitations !

Vous avez maintenant SMARTSAK10 installé comme une vraie application Windows !

**Prochaines étapes :**
1. Initialiser la base de données (automatique au premier lancement)
2. Créer vos classes
3. Inscrire vos élèves
4. Commencer à saisir les notes
5. Générer vos premiers bulletins !

---

**Version** : 1.0.0  
**Date** : Novembre 2024  
**Copyright** © 2024 SMARTSAK10
