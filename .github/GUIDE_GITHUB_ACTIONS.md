# 🤖 Guide GitHub Actions - Build Automatique du .exe

## 📋 Vue d'ensemble

Ce guide explique comment utiliser GitHub Actions pour créer automatiquement votre fichier `.exe` sans avoir besoin d'installer quoi que ce soit sur votre PC.

---

## ✨ Avantages

✅ **Aucune installation locale** (pas de Node.js, Python, etc.)
✅ **Build dans le cloud** (serveurs GitHub puissants)
✅ **Téléchargement direct** du .exe
✅ **Gratuit** (2000 minutes/mois pour comptes gratuits)
✅ **Automatique** à chaque commit
✅ **Reproductible** (même environnement à chaque fois)

---

## 🚀 Configuration Initiale (Une seule fois)

### Étape 1 : Créer un Repository GitHub

1. **Aller sur GitHub.com**
   - Se connecter ou créer un compte

2. **Créer un nouveau repository**
   - Cliquer sur `+` → `New repository`
   - Nom : `smartsak10`
   - Visibilité : `Private` (recommandé) ou `Public`
   - Cliquer `Create repository`

### Étape 2 : Push votre Code sur GitHub

**Option A : Via GitHub Desktop (Plus simple)**

1. Télécharger GitHub Desktop : https://desktop.github.com/
2. Se connecter avec votre compte
3. `File` → `Add Local Repository`
4. Sélectionner votre dossier `SMARTSAK10`
5. Cliquer `Publish repository`

**Option B : Via Ligne de Commande**

```bash
cd C:\SMARTSAK10
git init
git add .
git commit -m "Initial commit - SMARTSAK10"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/smartsak10.git
git push -u origin main
```

### Étape 3 : Vérifier les Workflows

Après le push, GitHub Actions détecte automatiquement les workflows dans `.github/workflows/`

1. Aller sur votre repository GitHub
2. Cliquer sur l'onglet `Actions`
3. Vous devriez voir 2 workflows :
   - **Build Windows EXE** (build complet)
   - **Test Build (Fast)** (tests rapides)

---

## 🎯 Utilisation

### Méthode 1 : Build Automatique (à chaque push)

**Quand :** À chaque fois que vous push du code sur `main` ou `master`

```bash
# Faites vos modifications
git add .
git commit -m "Mise à jour de l'application"
git push
```

**Résultat :** Le workflow démarre automatiquement

### Méthode 2 : Build Manuel (à la demande)

1. Aller sur GitHub.com → Votre repository
2. Cliquer sur `Actions`
3. Sélectionner `Build Windows EXE`
4. Cliquer sur `Run workflow`
5. Choisir la branche (`main`)
6. Cliquer sur `Run workflow` (vert)

### Méthode 3 : Build avec Release (recommandée pour versions)

**Créer une version numérotée :**

```bash
# Créer un tag
git tag v1.0.0
git push origin v1.0.0
```

**Résultat :** 
- Build automatique
- Création d'une Release GitHub
- .exe attaché à la Release

---

## 📥 Télécharger le .exe

### Depuis Actions (Artifacts)

1. Aller sur `Actions`
2. Cliquer sur le workflow terminé (✓ coche verte)
3. Descendre jusqu'à `Artifacts`
4. Cliquer sur `SMARTSAK10-Windows-Installer`
5. Le fichier ZIP se télécharge
6. Extraire le ZIP → Récupérer le .exe

**Note :** Les artifacts sont conservés 30 jours

### Depuis Releases (Tags)

Si vous avez créé un tag :

1. Aller sur l'onglet `Releases`
2. Cliquer sur la version (ex: `v1.0.0`)
3. Télécharger directement le .exe dans `Assets`

**Avantage :** Permanent, pas de limite de temps

---

## ⏱️ Temps de Build

**Durée typique :** 15-20 minutes

**Étapes :**
- Setup environnement : 2-3 min
- Install dépendances Backend : 3-4 min
- Install dépendances Frontend : 2-3 min
- Build Frontend : 2-3 min
- Préparer Electron : 1-2 min
- Build .exe : 5-7 min
- Upload artifact : 1-2 min

**Suivi en temps réel :**
- Aller sur `Actions`
- Cliquer sur le workflow en cours
- Voir les logs en direct

---

## 📊 Workflow Détaillé

### Build Windows EXE (Principal)

**Fichier :** `.github/workflows/build-windows-exe.yml`

**Trigger :**
- Push sur `main` ou `master`
- Création d'un tag `v*`
- Manuel via `workflow_dispatch`

**Étapes :**
1. ✅ Checkout du code
2. ✅ Setup Node.js 20
3. ✅ Setup Python 3.11
4. ✅ Cache des dépendances
5. ✅ Install Backend (pip)
6. ✅ Install Frontend (yarn)
7. ✅ Build React
8. ✅ Préparer Electron
9. ✅ Build .exe Windows
10. ✅ Upload artifact
11. ✅ Créer Release (si tag)

### Test Build (Rapide)

**Fichier :** `.github/workflows/test-build.yml`

**Trigger :**
- Pull Request
- Manuel

**Durée :** 5-7 minutes

**But :** Vérifier que tout compile sans créer le .exe complet

---

## 🔧 Configuration Avancée

### Changer le Nom du Fichier

Dans `electron-app/package.json` :

```json
"build": {
  "nsis": {
    "artifactName": "MonApp-Setup-${version}.${ext}"
  }
}
```

### Changer la Version

Dans `electron-app/package.json` :

```json
"version": "2.0.0"
```

Puis push le changement.

### Build Seulement sur Tag

Modifier `.github/workflows/build-windows-exe.yml` :

```yaml
on:
  push:
    tags:
      - 'v*'
```

### Notification par Email

Ajouter à la fin du workflow :

```yaml
- name: 📧 Send notification
  if: always()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Build ${{ job.status }}
    to: konatdra@gmail.com
    from: GitHub Actions
    body: Le build est ${{ job.status }}
```

---

## 🐛 Dépannage

### Le workflow échoue

1. **Vérifier les logs**
   - Aller sur `Actions`
   - Cliquer sur le workflow rouge
   - Lire les messages d'erreur

2. **Erreurs communes**

   **"Package.json not found"**
   ```
   → Vérifier que electron-app/package.json existe
   → Push le fichier manquant
   ```

   **"Out of memory"**
   ```
   → Normal sur GitHub Free
   → Retry le workflow
   → Ou upgrade vers GitHub Pro
   ```

   **"Dependencies failed"**
   ```
   → Vérifier requirements.txt
   → Vérifier package.json
   → Supprimer les dépendances problématiques
   ```

### Artifact non disponible

**Causes :**
- Le workflow a échoué
- Plus de 30 jours écoulés
- Artifact supprimé manuellement

**Solution :** Re-run le workflow

### Le .exe ne démarre pas

**Test localement d'abord :**
```bash
cd electron-app
npm start
```

Si ça fonctionne localement mais pas le .exe :
- Vérifier que MongoDB est installé
- Vérifier les permissions Windows

---

## 💰 Limites GitHub Actions

### Compte Gratuit
- ✅ 2000 minutes/mois
- ✅ Workflows publics : illimités
- ⚠️ Workflows privés : 2000 min/mois
- ⚠️ 1 workflow concurrent

**Calcul :**
- 1 build = ~20 minutes
- 2000 min / 20 = **100 builds/mois**
- Largement suffisant !

### GitHub Pro ($4/mois)
- ✅ 3000 minutes/mois
- ✅ Workflows prioritaires
- ✅ Plusieurs workflows simultanés

---

## 📋 Checklist

### Avant le premier build

- [ ] Repository GitHub créé
- [ ] Code pushé sur GitHub
- [ ] Fichiers `.github/workflows/` présents
- [ ] Branche `main` ou `master` existe

### Après chaque build

- [ ] Workflow terminé avec succès (✓)
- [ ] Artifact téléchargé
- [ ] .exe extrait du ZIP
- [ ] .exe testé sur un PC

### Pour une Release

- [ ] Version changée dans `package.json`
- [ ] Tag créé (`git tag v1.0.0`)
- [ ] Tag pushé (`git push origin v1.0.0`)
- [ ] Release créée automatiquement
- [ ] .exe attaché à la Release

---

## 🎯 Workflow Optimal

```
1. Développer localement
   └─ Tester avec yarn start

2. Commit et Push
   └─ git push origin main

3. GitHub Actions build automatiquement
   └─ Attendre 15-20 min

4. Télécharger l'artifact
   └─ Depuis l'onglet Actions

5. Tester le .exe
   └─ Sur un PC propre

6. Si OK, créer un tag
   └─ git tag v1.0.0 && git push origin v1.0.0

7. Distribuer depuis Releases
   └─ URL permanente pour utilisateurs
```

---

## 📞 Support

**GitHub Actions Documentation :**
https://docs.github.com/en/actions

**Electron Builder :**
https://www.electron.build/

**Questions :**
konatdra@gmail.com

---

## ✅ Résumé

✅ **Workflows créés** (2 fichiers)
✅ **Build automatique** configuré
✅ **Téléchargement direct** disponible
✅ **Releases** automatiques (sur tag)
✅ **Documentation** complète

**Prochaines étapes :**
1. Push le code sur GitHub
2. Attendre le build
3. Télécharger le .exe
4. Distribuer aux utilisateurs

🎉 **C'EST PRÊT !**
