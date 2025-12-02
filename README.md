# 🎓 SMARTSAK10 - Système de Management Scolaire

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)

**Application complète de gestion scolaire pour l'IEPP SAKASSOU, spécialisée dans la gestion des examens CEPE en Côte d'Ivoire 🇨🇮**

---

## 🚀 TÉLÉCHARGER LE .EXE

### Méthode Automatique (Recommandée) ⚡

**Pas besoin d'installer quoi que ce soit !**

1. Aller sur l'onglet **[Actions](../../actions)**
2. Cliquer sur le workflow **"Build Windows EXE"**
3. Cliquer sur le dernier build réussi (✅)
4. Télécharger **"SMARTSAK10-Windows-Installer"** dans Artifacts
5. Extraire le ZIP et installer le .exe

**OU depuis les Releases :**

1. Aller sur **[Releases](../../releases)**
2. Télécharger `SMARTSAK10-Setup-1.0.0.exe`
3. Installer et utiliser !

---

## ✨ Fonctionnalités Principales

- ✅ **Import Excel AGCEPE** (22 colonnes)
- ✅ **Import photos en masse** (ZIP par école)
- ✅ **Répartition CEPE intelligente** (tri alphabétique, règles métier)
- ✅ **4 modèles de cartes scolaires** vifs avec logo (8/page A4)
- ✅ **Statistiques multi-niveaux** (école, secteur, commune, sous-préfecture)
- ✅ **Gestion centres d'examen**
- ✅ **Secteurs pédagogiques**

---

## 📦 Installation

### Option 1 : Télécharger le .exe (Le plus simple)

➡️ **[Télécharger depuis Actions](../../actions)** ou **[Releases](../../releases)**

### Option 2 : Builder localement

```bash
git clone https://github.com/VOTRE_USERNAME/smartsak10.git
cd smartsak10
BUILD_INSTRUCTIONS_WINDOWS.bat
```

➡️ Le .exe sera dans `electron-app/dist/`

---

## 🛠️ Stack Technique

**Backend :** FastAPI + MongoDB + ReportLab  
**Frontend :** React 18 + Tailwind CSS + Shadcn UI  
**Desktop :** Electron + NSIS Installer  
**CI/CD :** GitHub Actions (build automatique)

---

## 📚 Documentation

- 📄 [Guide Installation Windows](GUIDE_INSTALLATION_WINDOWS.md)
- 📄 [Guide Création .exe](GUIDE_CREATION_EXE_WINDOWS.md)
- 📄 [Guide GitHub Actions](.github/GUIDE_GITHUB_ACTIONS.md)
- 📄 [Démarrage Rapide](START_HERE_WINDOWS.txt)

---

## 🤖 Build Automatique

Ce projet utilise **GitHub Actions** pour créer automatiquement le fichier .exe dans le cloud.

**À chaque push sur `main` :**
- Build automatique en 15-20 minutes
- .exe disponible dans Actions/Artifacts
- Aucune installation locale requise

**Pour créer une Release :**
```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 👥 Contact

**Organisation :** IEPP SAKASSOU  
**Région :** GBEKE, BOUAKE 2  
**Email :** konatdra@gmail.com

---

## 📜 Licence

© 2024 IEPP SAKASSOU - Tous droits réservés

---

<p align="center">
  <strong>🇨🇮 Fait avec ❤️ pour l'éducation en Côte d'Ivoire 🇨🇮</strong>
</p>
