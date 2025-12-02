# 🚀 SMARTSAK10 - Guide de Déploiement Complet

## 🎯 Vue d'ensemble du projet

**SMARTSAK10** est un système complet de gestion scolaire développé pour l'IEPP SAKASSOU, spécialisé dans la gestion des examens CEPE (Certificat d'Études Primaires Élémentaires).

### Architecture Technique

```
┌─────────────────────────────────────────┐
│         SMARTSAK10 - Stack Technique        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│            Frontend (React)              │
│   - React 18 + React Router            │
│   - Tailwind CSS + Shadcn UI           │
│   - Axios pour API calls               │
│   - Port: 3000                         │
└─────────────────────────────────────────┘
                    │
                    │ HTTP/REST
                    ↓
┌─────────────────────────────────────────┐
│          Backend (FastAPI)             │
│   - FastAPI + Uvicorn                 │
│   - Motor (async MongoDB driver)      │
│   - ReportLab (génération PDF)        │
│   - Port: 8001                         │
└─────────────────────────────────────────┘
                    │
                    │ MongoDB Protocol
                    ↓
┌─────────────────────────────────────────┐
│         Base de données (MongoDB)       │
│   - Collections: 10+                   │
│   - Index optimisés                    │
│   - Port: 27017                        │
└─────────────────────────────────────────┘
```

---

## 📦 Fonctionnalités Implémentées

### ✅ PHASE 1 - Infrastructure Complète

#### 1. **Paramètres Globaux**
- Année scolaire modifiable
- Configuration DRENA, IEPP, Région
- Session d'examen
- Gestion dates

#### 2. **Import de Données**
- **Import Excel AGCEPE** (22 colonnes)
  - Code DREN, Code IEPP, Code école
  - Matricule, Nom, Prénoms, Sexe
  - Date de naissance (jour, mois, année)
  - Nationalité, Localité, Sous-préfecture
  - Père, Mère, Acte de naissance
  - Niveau (CM2 pour CEPE)

- **Import Photos en Masse**
  - Format ZIP par école
  - Nommage par matricule (ex: 12345.jpg)
  - Statistiques temps réel

- **Épuration Doublons**
  - Mode automatique
  - Mode manuel avec validation

#### 3. **Secteurs Pédagogiques**
- Import Excel (2 colonnes: SECTEUR | ÉCOLES)
- Gestion manuelle des secteurs
- Attribution écoles aux secteurs

#### 4. **Statistiques Résultats**
- **Multi-niveaux :**
  - Par école
  - Par secteur pédagogique
  - Par commune
  - Par sous-préfecture

- **Indicateurs :**
  - Total candidats
  - Admis / Ajournés
  - Taux de réussite
  - Moyenne générale
  - Répartition mentions

#### 5. **Cartes Scolaires**
- **4 Modèles Vifs avec Logo :**
  1. Standard Bleu-Vert Vif
  2. Violet Vif avec Logo
  3. Orange-Jaune Vif avec Logo
  4. Drapeau Ivoirien 🇨🇮 avec Logo

- **Format :** 8 cartes par page A4
- **Contenu :**
  - Photo candidat
  - Matricule
  - Nom et Prénoms
  - Date de naissance
  - Nom de l'école
  - Niveau et Classe
  - Logo IEPP SAKASSOU (filigrane + petit logo)
  - Emplacement émargement directeur

### ✅ PHASE 2 - Répartition CEPE Complète

#### 1. **Gestion Centres d'Examen**
- Création/modification centres
- Capacité max : 480 candidats
- Salles fonctionnelles : max 16

#### 2. **Affectation Écoles → Centres**
- Mode manuel (dropdown)
- Affectation temps réel
- Visualisation affectations

#### 3. **Algorithme de Répartition Intelligent**
- **Tri alphabétique** des candidats CM2
- **Règles métier respectées :**
  - 28 candidats/salle (sauf dernière)
  - 29-30 autorisés si effectif école > 28
  - Max 16 salles/centre
  - Max 480 candidats/centre

#### 4. **Export Multi-Format**
- CSV
- Excel (prévu)
- PDF (prévu)

---

## 📊 Base de Données MongoDB

### Collections Créées

```javascript
// 1. candidats_cepe
{
  id: String,
  matricule: String (index unique + annee_scolaire),
  nom: String,
  prenoms: String,
  sexe: "M" | "F",
  date_naissance: Date,
  ecole: String (index),
  niveau: String (index),
  photo_url: String,
  annee_scolaire: String
}

// 2. centres_composition
{
  id: String,
  nom: String,
  capacite_max: Number,
  nb_salles_fonctionnelles: Number,
  ecoles_affectees: [String],
  annee_scolaire: String (index)
}

// 3. secteurs_pedagogiques
{
  id: String,
  nom: String (index + annee_scolaire),
  ecoles: [String],
  annee_scolaire: String
}

// 4. resultats_compositions
{
  id: String,
  candidat_id: String (index + type_examen),
  type_examen: String,
  notes: Object,
  note_eps: Number,
  moyenne: Number,
  mention: String,
  admis: Boolean,
  ecole: String (index),
  annee_scolaire: String (index)
}

// 5. parametres
{
  annee_scolaire_actuelle: String,
  session_examen: String,
  drena: String,
  iepp: String,
  region: String
}
```

### Index Optimisés

```javascript
// Créés automatiquement via create_indexes.py
- candidats_cepe: {matricule: 1, annee_scolaire: 1} (unique)
- candidats_cepe: {ecole: 1}
- candidats_cepe: {niveau: 1}
- candidats_cepe: {nom: 1, prenoms: 1}
- resultats_compositions: {candidat_id: 1, type_examen: 1}
- resultats_compositions: {ecole: 1}
- centres_composition: {annee_scolaire: 1}
- secteurs_pedagogiques: {nom: 1, annee_scolaire: 1}
```

---

## 🛣️ Routes API (43 endpoints)

### Paramètres
```
GET    /api/parametres/
PUT    /api/parametres/
```

### Import
```
POST   /api/import/excel/candidats
POST   /api/import/photos/zip
GET    /api/import/candidats/stats
POST   /api/import/epuration/doublons
```

### Centres d'Examen
```
GET    /api/centres/
POST   /api/centres/
GET    /api/centres/{centre_id}
PUT    /api/centres/{centre_id}
DELETE /api/centres/{centre_id}
POST   /api/centres/{centre_id}/affecter-ecole
DELETE /api/centres/{centre_id}/retirer-ecole/{codeecole}
```

### Secteurs Pédagogiques
```
GET    /api/secteurs/
POST   /api/secteurs/
POST   /api/secteurs/import/excel
POST   /api/secteurs/{secteur_id}/ajouter-ecole
DELETE /api/secteurs/{secteur_id}/retirer-ecole
```

### Résultats & Statistiques
```
POST   /api/resultats/composition
GET    /api/resultats/statistiques/ecole/{ecole}
GET    /api/resultats/statistiques/secteur/{secteur}
GET    /api/resultats/statistiques/commune/{commune}
GET    /api/resultats/statistiques/sous-prefecture/{sp}
```

### Cartes Scolaires
```
POST   /api/cartes/generer
```

### Répartition
```
POST   /api/repartition/calculer
GET    /api/repartition/repartition
GET    /api/repartition/export
```

---

## 📦 Options de Déploiement

### Option 1 : Application de Bureau Windows (Recommandé)

**Avantages :**
- ✅ Utilisation hors ligne
- ✅ Pas besoin de serveur
- ✅ Installation simple (.exe)
- ✅ Icône sur le bureau

**Procédure :**
1. Exécuter `BUILD_INSTRUCTIONS_WINDOWS.bat`
2. Installer MongoDB localement
3. Distribuer `SMARTSAK10-Setup.exe`

**Fichiers nécessaires :**
- `electron-app/main.js`
- `electron-app/package.json`
- `BUILD_INSTRUCTIONS_WINDOWS.bat`
- `INSTALLER_MONGODB_WINDOWS.bat`
- `LANCER_APPLICATION.bat`

### Option 2 : Déploiement Cloud (Emergent/K8s)

**Avantages :**
- ✅ Accès depuis n'importe où
- ✅ Mises à jour centralisées
- ✅ Sauvegarde automatique
- ✅ Pas d'installation client

**Fichiers prêts :**
- ✅ `/app/backend/.env`
- ✅ `/app/frontend/.env`
- ✅ `/etc/supervisor/conf.d/supervisord.conf`
- ✅ Index MongoDB créés

**Variables d'environnement :**
```env
# Backend
MONGO_URL=mongodb://localhost:27017  # Auto-update par Emergent
DB_NAME=smartscool
CORS_ORIGINS=*
AUTHORIZED_EMAIL=konatdra@gmail.com

# Frontend
REACT_APP_BACKEND_URL=http://localhost:8001  # Auto-update par Emergent
REACT_APP_USER_EMAIL=konatdra@gmail.com
```

### Option 3 : Installation Manuelle Serveur

**Pour serveur dédié :**

```bash
# 1. Installer dépendances
sudo apt update
sudo apt install python3-pip nodejs npm mongodb

# 2. Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 create_indexes.py

# 3. Frontend
cd frontend
npm install -g yarn
yarn install
yarn build

# 4. Lancer
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001
```

---

## ⚙️ Configuration

### Ports Utilisés
- **Frontend** : 3000
- **Backend** : 8001
- **MongoDB** : 27017

### Authentification
- **Email autorisé** : konatdra@gmail.com
- **Mode** : Simple email check (pas de mot de passe)

### Dossiers Importants
```
/app/
├── backend/
│   ├── routes/          # 9 modules de routes
│   ├── server.py        # Serveur FastAPI
│   ├── models_cepe.py   # Modèles Pydantic
│   ├── create_indexes.py
│   ├── .env
│   └── uploads/photos/  # Photos candidats
│
├── frontend/
│   ├── src/
│   │   ├── pages/       # 5 pages principales
│   │   ├── components/
│   │   └── services/
│   └── .env
│
└── electron-app/     # Package Windows
```

---

## 🛡️ Sécurité

### Implémenté
- ✅ Authentification par email
- ✅ CORS configuré
- ✅ Variables d'environnement
- ✅ Pas de hardcoding

### Recommandations Production
- [ ] Ajouter HTTPS
- [ ] Implémenter JWT tokens
- [ ] Rate limiting API
- [ ] Backup automatique MongoDB
- [ ] Logs centralisés

---

## 📊 Performance

### Optimisations Implémentées
- ✅ Index MongoDB
- ✅ Async/await (Motor)
- ✅ Pagination (to_list limits)
- ✅ Temps réponse : ~50ms

### À Améliorer
- [ ] Fix N+1 queries (note_routes, bulletin_routes)
- [ ] Cache Redis pour stats
- [ ] CDN pour assets statiques

---

## 📝 Documentation

### Fichiers créés
1. `GUIDE_INSTALLATION_WINDOWS.md` - Guide utilisateur complet
2. `README_DEPLOYMENT.md` - Ce fichier
3. `BUILD_INSTRUCTIONS_WINDOWS.bat` - Script build Windows
4. `INSTALLER_MONGODB_WINDOWS.bat` - Script MongoDB
5. `LANCER_APPLICATION.bat` - Lanceur rapide

### API Documentation
- OpenAPI/Swagger : `http://localhost:8001/docs`
- ReDoc : `http://localhost:8001/redoc`

---

## ✅ Checklist Déploiement

### Pré-déploiement
- [x] Backend fonctionnel
- [x] Frontend fonctionnel
- [x] MongoDB connecté
- [x] Toutes routes testées
- [x] Index créés
- [x] Variables .env configurées
- [x] Supervisor configuré
- [x] Documentation complète

### Post-déploiement
- [ ] Test charges (50+ utilisateurs simultanés)
- [ ] Backup stratégie définie
- [ ] Monitoring mis en place
- [ ] Plan de reprise après sinistre

---

## 📞 Support

**Contact :** konatdra@gmail.com  
**Organisation :** IEPP SAKASSOU  
**Version :** 1.0.0  
**Année :** 2024-2025

---

© 2024 SMARTSAK10 - Tous droits réservés
