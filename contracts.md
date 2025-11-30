# Contrats API - SmartScool Clone

## 1. API Endpoints

### Authentication APIs
- **POST /api/auth/register** - Inscription
  - Body: `{ name, email, password, phone, company }`
  - Response: `{ id, name, email, token }`

- **POST /api/auth/login** - Connexion
  - Body: `{ email, password }`
  - Response: `{ id, name, email, token }`

- **GET /api/auth/me** - Profil utilisateur
  - Headers: `Authorization: Bearer {token}`
  - Response: `{ id, name, email, phone, company }`

### Download APIs
- **GET /api/downloads** - Liste des fichiers disponibles
  - Response: `[{ id, name, version, size, type, url, date }]`

- **POST /api/downloads/track** - Enregistrer un téléchargement
  - Body: `{ downloadId, userId (optional) }`
  - Response: `{ success: true, downloadUrl }`

### Product APIs
- **GET /api/products** - Liste des produits
  - Response: `[{ id, name, description, features[], image }]`

- **GET /api/products/:id** - Détail d'un produit
  - Response: `{ id, name, description, features[], image, price }`

### Order APIs
- **POST /api/orders** - Créer une commande
  - Body: `{ name, email, phone, company, product, quantity, message }`
  - Response: `{ id, orderNumber, status, createdAt }`

- **GET /api/orders** - Liste des commandes (admin)
  - Headers: `Authorization: Bearer {token}`
  - Response: `[{ id, orderNumber, customerName, product, quantity, status }]`

- **GET /api/orders/:id** - Détail d'une commande
  - Headers: `Authorization: Bearer {token}`
  - Response: `{ id, orderNumber, customerInfo, product, quantity, message, status, createdAt }`

### Support/Ticket APIs
- **POST /api/tickets** - Créer un ticket
  - Body: `{ name, email, subject, priority, description }`
  - Response: `{ id, ticketNumber, status, createdAt }`

- **GET /api/tickets** - Liste des tickets (admin)
  - Headers: `Authorization: Bearer {token}`
  - Response: `[{ id, ticketNumber, name, subject, priority, status }]`

- **GET /api/tickets/:id** - Détail d'un ticket
  - Headers: `Authorization: Bearer {token}`
  - Response: `{ id, ticketNumber, name, email, subject, priority, description, status, createdAt }`

## 2. Modèles MongoDB

### User
```
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  password: String (hashed),
  phone: String,
  company: String,
  role: String (user/admin),
  createdAt: Date
}
```

### Download
```
{
  _id: ObjectId,
  name: String,
  version: String,
  size: String,
  type: String (kit_complet/mise_a_jour/ancienne_version),
  fileUrl: String,
  releaseDate: Date,
  downloads: Number
}
```

### Product
```
{
  _id: ObjectId,
  name: String,
  description: String,
  features: [String],
  image: String,
  price: Number,
  active: Boolean
}
```

### Order
```
{
  _id: ObjectId,
  orderNumber: String (auto-generated),
  name: String,
  email: String,
  phone: String,
  company: String,
  product: String,
  quantity: Number,
  message: String,
  status: String (pending/processing/completed),
  createdAt: Date
}
```

### Ticket
```
{
  _id: ObjectId,
  ticketNumber: String (auto-generated),
  name: String,
  email: String,
  subject: String,
  priority: String (low/normal/high/urgent),
  description: String,
  status: String (open/in_progress/resolved/closed),
  createdAt: Date,
  updatedAt: Date
}
```

## 3. Modifications Frontend Nécessaires

### Pages à modifier:

**Download.jsx**
- Remplacer `handleDownload` mock par appel API `POST /api/downloads/track`
- Récupérer la liste des fichiers depuis `GET /api/downloads`

**Login.jsx**
- Remplacer `handleSubmit` mock par appel API `POST /api/auth/login`
- Stocker le token dans localStorage
- Créer un AuthContext pour gérer l'état d'authentification

**Products.jsx**
- Remplacer products mockés par appel API `GET /api/products`

**Order.jsx**
- Remplacer `handleSubmit` mock par appel API `POST /api/orders`
- Afficher message de confirmation avec numéro de commande

**Support.jsx**
- Remplacer `handleSubmit` mock par appel API `POST /api/tickets`
- Afficher message de confirmation avec numéro de ticket

### Nouveaux fichiers à créer:
- `/frontend/src/context/AuthContext.jsx` - Gestion de l'authentification
- `/frontend/src/services/api.js` - Service API centralisé
- `/frontend/src/utils/auth.js` - Utilitaires d'authentification

## 4. Intégration Frontend-Backend

### Configuration
- Backend URL: Utiliser `process.env.REACT_APP_BACKEND_URL`
- Toutes les routes API préfixées par `/api`

### Gestion des erreurs
- Intercepteur axios pour gérer les erreurs 401 (redirect login)
- Messages d'erreur utilisateur-friendly
- Loading states pour toutes les requêtes

### Authentification
- JWT tokens stockés dans localStorage
- Header `Authorization: Bearer {token}` pour routes protégées
- Vérification du token à chaque chargement de page

## 5. Fichiers Upload

### Gestion des fichiers de téléchargement
- Stockage des fichiers dans `/app/backend/uploads/downloads/`
- URLs de téléchargement: `/api/downloads/file/:filename`
- Support des gros fichiers (chunked uploads si nécessaire)

## 6. Sécurité

- Hashing des mots de passe avec bcrypt
- Validation des inputs côté backend
- CORS configuré correctement
- Rate limiting sur les endpoints sensibles
- Sanitization des données utilisateur
