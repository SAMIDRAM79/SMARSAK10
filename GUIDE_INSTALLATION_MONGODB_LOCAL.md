# 🗄️ Installation de MongoDB en Local pour SMARTSAK10

## Pour utiliser SMARTSAK10 100% HORS LIGNE

---

## 🎯 Pourquoi MongoDB Local ?

✅ **Aucune connexion internet nécessaire**
✅ **Données stockées sur votre PC**
✅ **Accès rapide et sécurisé**
✅ **Gratuit et illimité**

---

## 📥 Téléchargement et Installation

### Windows :

1. **Télécharger MongoDB Community Server**
   - Aller sur : https://www.mongodb.com/try/download/community
   - Choisir : Windows x64
   - Version : Latest (7.0+)
   - Package : MSI

2. **Installer MongoDB**
   ```
   - Double-cliquer sur le fichier .msi téléchargé
   - Choisir "Complete" installation
   - IMPORTANT : Cocher "Install MongoDB as a Service"
   - IMPORTANT : Cocher "Install MongoDB Compass" (interface graphique)
   - Laisser le port par défaut : 27017
   - Terminer l'installation
   ```

3. **Vérifier l'installation**
   ```bash
   # Ouvrir CMD ou PowerShell
   mongod --version
   
   # Devrait afficher : db version v7.0.x
   ```

4. **Démarrer MongoDB (si pas démarré automatiquement)**
   ```bash
   # Option 1 : Via Services Windows
   - Appuyer sur Win+R
   - Taper : services.msc
   - Chercher "MongoDB"
   - Clic droit → Démarrer
   
   # Option 2 : Via ligne de commande
   net start MongoDB
   ```

---

## ✅ Configuration de SMARTSAK10

### Vérifier la configuration (déjà faite normalement) :

Fichier : `/app/backend/.env`

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=smartscool
```

✅ **Cette configuration signifie : 100% LOCAL, PAS D'INTERNET REQUIS**

---

## 🗂️ Initialiser la base de données

### Première utilisation - Créer les données de démo :

```bash
# Ouvrir terminal dans /app/backend
cd /app/backend

# Exécuter le script d'initialisation
python seed_smartsak10.py
```

**Résultat** :
- 12 classes créées
- 15 matières créées
- 4 enseignants créés
- 5 élèves de démonstration créés

---

## 🛠️ Gestion de MongoDB

### MongoDB Compass (Interface Graphique)

MongoDB Compass est installé avec MongoDB et permet de :
- Visualiser toutes vos données
- Créer/modifier/supprimer des documents
- Faire des recherches
- Exporter/importer des données

**Lancer Compass** :
1. Chercher "MongoDB Compass" dans le menu Démarrer
2. Connexion automatique à : `mongodb://localhost:27017`
3. Sélectionner la base : `smartscool`
4. Explorer les collections : students, classes, matieres, notes, etc.

### Commandes utiles

```bash
# Démarrer MongoDB
net start MongoDB

# Arrêter MongoDB
net stop MongoDB

# Redémarrer MongoDB
net stop MongoDB && net start MongoDB

# Vérifier le statut
sc query MongoDB
```

---

## 💾 Sauvegarde et Restauration

### Sauvegarder vos données (IMPORTANT !)

```bash
# Créer un dossier de sauvegarde
mkdir C:\SMARTSAK10_Backups

# Sauvegarder la base
mongodump --db smartscool --out C:\SMARTSAK10_Backups\backup_2024_11_30

# La sauvegarde contient toutes vos données :
# - Élèves
# - Notes
# - Bulletins
# - Classes
# - Enseignants
# etc.
```

### Restaurer une sauvegarde

```bash
# Restaurer depuis une sauvegarde
mongorestore --db smartscool C:\SMARTSAK10_Backups\backup_2024_11_30\smartscool
```

---

## 📊 Emplacement des données

### Où sont stockées vos données ?

Par défaut sur Windows :
```
C:\Program Files\MongoDB\Server\7.0\data\
```

**Taille approximative** :
- Installation vide : ~50 MB
- Avec 100 élèves : ~100 MB
- Avec 1000 élèves : ~500 MB

---

## 🔒 Sécurité (Optionnel)

### Ajouter un mot de passe à MongoDB

Par défaut, MongoDB local n'a pas de mot de passe (suffisant pour usage personnel).

Si vous voulez sécuriser :

1. **Créer un utilisateur admin**
   ```javascript
   // Dans MongoDB Compass ou shell
   use admin
   db.createUser({
     user: "admin",
     pwd: "VotreMotDePasse",
     roles: ["root"]
   })
   ```

2. **Modifier .env de SMARTSAK10**
   ```env
   MONGO_URL=mongodb://admin:VotreMotDePasse@localhost:27017
   ```

---

## 🐛 Dépannage

### MongoDB ne démarre pas

**Problème** : Erreur "MongoDB service failed to start"

**Solutions** :
1. Vérifier que le port 27017 n'est pas utilisé
   ```bash
   netstat -ano | findstr :27017
   ```

2. Vérifier les permissions du dossier data
   - Aller dans : C:\Program Files\MongoDB\Server\7.0\data\
   - Clic droit → Propriétés → Sécurité
   - S'assurer que votre utilisateur a les droits de lecture/écriture

3. Réinstaller MongoDB en tant qu'administrateur

### Erreur "Connection refused"

**Solutions** :
1. Vérifier que MongoDB est démarré :
   ```bash
   sc query MongoDB
   ```

2. Redémarrer le service :
   ```bash
   net stop MongoDB
   net start MongoDB
   ```

3. Vérifier que le firewall ne bloque pas le port 27017

### Erreur "Database not found"

**Solution** :
```bash
# Réinitialiser la base
cd /app/backend
python seed_smartsak10.py
```

---

## 📱 MongoDB Atlas (Cloud) - Alternative avec INTERNET

Si vous voulez synchroniser entre plusieurs PC ou accéder à distance :

### Avantages :
✅ Accessible depuis n'importe où
✅ Sauvegarde automatique
✅ Gratuit jusqu'à 512 MB

### Inconvénients :
❌ Nécessite une connexion internet
❌ Limité en espace (gratuit)

### Configuration :

1. Créer un compte sur : https://www.mongodb.com/cloud/atlas
2. Créer un cluster gratuit
3. Obtenir la connexion string
4. Modifier `/app/backend/.env` :
   ```env
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/smartscool?retryWrites=true&w=majority
   ```

---

## ✅ Résumé - Usage OFFLINE

Pour utiliser SMARTSAK10 **100% SANS INTERNET** :

1. ✅ Installer MongoDB local
2. ✅ Garder MONGO_URL=mongodb://localhost:27017 dans .env
3. ✅ Démarrer MongoDB avant de lancer SMARTSAK10
4. ✅ Initialiser les données avec seed_smartsak10.py
5. ✅ Utiliser l'application normalement !

---

## 📞 Support

Pour toute question sur MongoDB :
- Documentation : https://www.mongodb.com/docs/
- Email : konatdra@gmail.com

---

**Date** : Novembre 2024
**Version MongoDB recommandée** : 7.0+
**Compatible avec** : SMARTSAK10 v1.0.0
