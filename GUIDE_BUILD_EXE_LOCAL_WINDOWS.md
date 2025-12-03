# 🚀 GUIDE COMPLET : Construire SMARTSAK10.exe sur Windows

## ⏱️ Temps estimé : 30-60 minutes

---

## 📋 ÉTAPE 1 : Installations requises (À faire UNE SEULE FOIS)

### 1.1 - Installer Node.js

1. Allez sur : https://nodejs.org/
2. Téléchargez la version **LTS** (recommandée)
3. Exécutez l'installateur
4. Cliquez sur "Next" jusqu'à la fin
5. Redémarrez votre ordinateur

**Vérification :**
- Ouvrez un CMD (Windows + R, tapez `cmd`, Entrée)
- Tapez : `node --version`
- Vous devriez voir : `v20.x.x` ou similaire

---

### 1.2 - Installer Python

1. Allez sur : https://www.python.org/downloads/
2. Téléchargez **Python 3.11** (ou version supérieure)
3. **IMPORTANT** : Cochez "Add Python to PATH" avant d'installer
4. Cliquez sur "Install Now"
5. Attendez la fin de l'installation

**Vérification :**
- Ouvrez un CMD
- Tapez : `python --version`
- Vous devriez voir : `Python 3.11.x` ou similaire

---

### 1.3 - Installer Git

1. Allez sur : https://git-scm.com/download/win
2. Téléchargez la version Windows
3. Exécutez l'installateur
4. Cliquez sur "Next" (gardez les options par défaut)

**Vérification :**
- Ouvrez un CMD
- Tapez : `git --version`
- Vous devriez voir : `git version 2.x.x`

---

### 1.4 - Installer Yarn

1. Ouvrez un CMD **en tant qu'Administrateur** :
   - Cliquez droit sur le menu Démarrer
   - Choisissez "Terminal (Admin)" ou "PowerShell (Admin)"

2. Tapez cette commande :
```bash
npm install -g yarn
```

3. Attendez la fin de l'installation

**Vérification :**
- Tapez : `yarn --version`
- Vous devriez voir : `1.22.x` ou similaire

---

## 📥 ÉTAPE 2 : Télécharger le projet depuis GitHub

### 2.1 - Créer un dossier pour le projet

1. Ouvrez l'Explorateur Windows
2. Créez un dossier, par exemple : `C:\SMARTSAK10`

---

### 2.2 - Ouvrir le terminal dans ce dossier

1. Ouvrez le dossier `C:\SMARTSAK10`
2. Dans la barre d'adresse, tapez `cmd` et appuyez sur Entrée
3. Un terminal s'ouvre dans ce dossier

---

### 2.3 - Cloner le projet

Dans le terminal, tapez :

```bash
git clone https://github.com/SAMIDRAM79/SMARSAK10.git
```

Attendez que le téléchargement se termine.

---

### 2.4 - Entrer dans le dossier du projet

```bash
cd SMARSAK10
```

---

## 🔧 ÉTAPE 3 : Installer les dépendances

### 3.1 - Installer les dépendances Backend (Python)

Dans le terminal, tapez ces commandes **UNE PAR UNE** :

```bash
cd backend
```

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

Vous devriez voir `(venv)` apparaître au début de la ligne.

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

**⚠️ IMPORTANT** : Cette étape peut prendre 5-10 minutes. Soyez patient !

Une fois terminé, tapez :

```bash
cd ..
```

(Pour revenir au dossier principal)

---

### 3.2 - Installer les dépendances Frontend (React)

```bash
cd frontend
```

```bash
yarn install
```

**⚠️ IMPORTANT** : Cette étape peut prendre 5-10 minutes. Soyez patient !

Une fois terminé, tapez :

```bash
cd ..
```

---

### 3.3 - Installer les dépendances Electron

```bash
cd electron-app
```

```bash
yarn install
```

Attendez la fin de l'installation.

Une fois terminé, tapez :

```bash
cd ..
```

---

## 🏗️ ÉTAPE 4 : Construire l'application

### 4.1 - Construire le Frontend

```bash
cd frontend
```

```bash
yarn build
```

**⚠️ IMPORTANT** : Cette étape peut prendre 2-5 minutes.

Vous verrez beaucoup de texte défiler. C'est normal !

Une fois terminé (vous verrez "Compiled successfully"), tapez :

```bash
cd ..
```

---

### 4.2 - Préparer la structure Electron

Nous allons copier les fichiers nécessaires dans le dossier electron-app.

**Copiez le frontend buildé :**

```bash
xcopy /E /I /Y frontend\build electron-app\frontend-build
```

**Copiez le backend :**

```bash
xcopy /E /I /Y backend electron-app\backend
```

**Copiez Python :**

```bash
xcopy /E /I /Y backend\venv electron-app\python
```

---

## 🎯 ÉTAPE 5 : Construire le fichier .exe

### 5.1 - Entrer dans le dossier electron-app

```bash
cd electron-app
```

---

### 5.2 - Lancer la construction du .exe

```bash
yarn build:win
```

**⚠️ CETTE ÉTAPE PEUT PRENDRE 10-20 MINUTES !**

Vous verrez beaucoup de texte défiler. C'est normal ! Soyez TRÈS patient.

À la fin, vous verrez quelque chose comme :
```
• building        target=nsis file=SMARTSAK10 Setup 1.0.0.exe
```

---

## 🎊 ÉTAPE 6 : Trouver votre fichier .exe

Votre fichier .exe se trouve dans :

```
C:\SMARTSAK10\SMARSAK10\electron-app\dist\
```

Le fichier s'appelle :
```
SMARTSAK10 Setup 1.0.0.exe
```

---

## ✅ ÉTAPE 7 : Installer l'application

1. Double-cliquez sur `SMARTSAK10 Setup 1.0.0.exe`
2. Suivez les instructions d'installation
3. L'application sera installée sur votre ordinateur
4. Un raccourci sera créé sur votre Bureau

---

## 🆘 EN CAS DE PROBLÈME

### Erreur : "node n'est pas reconnu..."
➜ Node.js n'est pas installé ou pas dans le PATH. Réinstallez Node.js.

### Erreur : "python n'est pas reconnu..."
➜ Python n'est pas installé ou pas dans le PATH. Réinstallez Python et cochez "Add to PATH".

### Erreur : "yarn n'est pas reconnu..."
➜ Exécutez : `npm install -g yarn` en tant qu'administrateur.

### L'installation prend trop de temps
➜ C'est normal ! La construction d'un .exe peut prendre 10-20 minutes.

### Le fichier .exe n'existe pas après le build
➜ Vérifiez les erreurs dans le terminal. Envoyez-moi une capture d'écran du message d'erreur.

---

## 📞 BESOIN D'AIDE ?

Si vous rencontrez un problème :
1. Prenez une capture d'écran du message d'erreur
2. Notez à quelle étape vous êtes bloqué
3. Contactez-moi avec ces informations

---

## 🎉 FÉLICITATIONS !

Une fois l'installation terminée, vous aurez SMARTSAK10 sur votre ordinateur Windows !

L'application fonctionnera comme une vraie application de bureau. 🚀
