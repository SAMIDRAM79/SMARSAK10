# SMARTSAK10 - Application Desktop Windows

## Système de Gestion Scolaire Complet

Application desktop native pour Windows permettant de gérer votre établissement scolaire (Pré-primaire, Maternelle, Primaire).

## 🚀 Installation pour l'utilisateur final

### Option 1 : Installer depuis le fichier .exe (RECOMMANDÉ)

1. Téléchargez le fichier `SMARTSAK10 Setup 1.0.0.exe` depuis le dossier `dist`
2. Double-cliquez sur le fichier
3. Suivez l'assistant d'installation
4. Une fois installé, lancez SMARTSAK10 depuis le bureau ou le menu démarrer

### Option 2 : Version portable (sans installation)

1. Téléchargez le dossier `win-unpacked` depuis `dist`
2. Copiez le dossier où vous voulez
3. Lancez `SMARTSAK10.exe`

## 📋 Prérequis (déjà inclus dans l'installateur)

- Windows 7 ou supérieur (64-bit)
- Python 3.8+ (sera installé automatiquement si nécessaire)
- Node.js 16+ (sera installé automatiquement si nécessaire)

## 🔧 Construction de l'application (Pour développeurs)

### Prérequis de développement

1. **Python 3.11+** installé et dans le PATH
2. **Node.js 16+** et Yarn installés
3. **MongoDB** local ou distant

### Étapes de build

```bash
# 1. Installer les dépendances
cd /app/electron-app
yarn install

# 2. Construire l'application Windows
yarn dist:win

# Le fichier .exe sera dans : /app/electron-app/dist/
```

### Build rapide (sans empaquetage)

```bash
# Pour tester sans créer le .exe
yarn pack
```

## 🎯 Fonctionnalités

### Modules inclus :
- ✅ **Tableau de bord** : Statistiques en temps réel
- ✅ **Gestion des élèves** : Inscription, profils, photos
- ✅ **Gestion des classes** : 12 classes (PS1, PS2, MS1, MS2, GS1, GS2, CP1, CP2, CE1, CE2, CM1, CM2)
- ✅ **Gestion des notes** : Exploitation de texte/50, Éveil au milieu/50, Dictée/20, Mathématiques/50, EPS/20
- ✅ **Bulletins scolaires** : Génération automatique avec moyennes, rang, appréciations
- ✅ **Cartes scolaires** : Génération de cartes pour les élèves
- ✅ **Fiches EPS** : Suivi physique des élèves
- ✅ **Gestion des enseignants** : Personnel et affectations
- ✅ **Emploi du temps** : Planning des cours
- ✅ **Comptabilité** : Frais scolaires et paiements
- ✅ **Rapports** : Statistiques détaillées

## 🔐 Connexion

**Email administrateur** : konatdra@gmail.com

(Configuré dans le code, modifiable dans `/app/backend/.env`)

## 📁 Structure des fichiers

```
SMARTSAK10/
├── backend/          # API FastAPI
│   ├── server.py
│   ├── routes/
│   └── models.py
├── frontend/         # Interface React
│   ├── src/
│   └── public/
└── electron-app/     # Application Desktop
    ├── main.js
    └── package.json
```

## 🐛 Dépannage

### L'application ne démarre pas

1. Vérifiez que Python est installé : `python --version`
2. Vérifiez que Node.js est installé : `node --version`
3. Vérifiez les logs dans : `%APPDATA%/smartsak10/logs`

### Erreur de connexion à la base de données

1. Assurez-vous que MongoDB est installé et démarré
2. Vérifiez la configuration dans `/app/backend/.env`
3. Par défaut : `mongodb://localhost:27017`

### Le frontend ne charge pas

1. Attendez 30-60 secondes au premier démarrage (compilation)
2. Vérifiez que le port 3000 n'est pas utilisé par une autre application
3. Redémarrez l'application

## 📞 Support

Pour toute question ou problème :
- Email : konatdra@gmail.com

## 📝 Licence

Copyright © 2024 SMARTSAK10

---

**Version** : 1.0.0
**Date** : Novembre 2024
