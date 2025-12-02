# 🚀 GUIDE RAPIDE - Résoudre l'erreur GitHub Actions

## 📦 CE QUE VOUS DEVEZ FAIRE (5 MINUTES)

### 1️⃣ Télécharger l'archive
- Fichier : `SMARTSAK10_COMPLET.zip` ou `SMARTSAK10_COMPLET.tar.gz`
- Extrayez dans un dossier (ex: `C:\SMARTSAK10`)

### 2️⃣ Ouvrir le terminal
- Dans l'Explorateur Windows, allez dans le dossier extrait
- Tapez `cmd` dans la barre d'adresse
- Appuyez sur Entrée

### 3️⃣ Copier-coller ces commandes

**Initialisez Git :**
```bash
git init
```

**Liez votre repository GitHub** (remplacez par votre URL) :
```bash
git remote add origin https://github.com/VOTRE_NOM/VOTRE_REPO.git
```

**Exemple :**
```bash
git remote add origin https://github.com/konatdra/smartsak10.git
```

**Ajoutez tous les fichiers :**
```bash
git add .
```

**Créez le commit :**
```bash
git commit -m "Ajout yarn.lock et mise à jour"
```

**Poussez sur GitHub :**
```bash
git push -u origin main
```

### 4️⃣ Authentification GitHub

Si demandé :
- **Username** : Votre nom d'utilisateur GitHub
- **Password** : Utilisez un **Personal Access Token**

**Comment obtenir le token :**
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Cochez "repo"
4. Copiez le token généré
5. Utilisez-le comme mot de passe

### 5️⃣ Vérifier le résultat

1. Allez sur votre repo GitHub
2. Onglet **"Actions"**
3. Le workflow devrait se lancer automatiquement
4. Après quelques minutes, téléchargez le `.exe` dans "Artifacts"

---

## ✅ C'EST TOUT !

Une fois ces étapes effectuées, votre fichier `.exe` sera construit automatiquement par GitHub.

---

## 🆘 Besoin d'aide ?

Consultez le fichier `INSTRUCTIONS_PUSH_GITHUB.md` pour des instructions détaillées avec résolution de problèmes.
