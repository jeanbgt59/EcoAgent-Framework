# Documentation API

## Endpoints disponibles

### Health Check
- GET /api/v1/health - Vérifie l'état de l'application

### Utilisateurs
- GET /api/v1/users - Liste des utilisateurs
- POST /api/v1/users - Créer un utilisateur
- GET /api/v1/users/{id} - Détails d'un utilisateur
- PUT /api/v1/users/{id} - Modifier un utilisateur
- DELETE /api/v1/users/{id} - Supprimer un utilisateur

### Items
- GET /api/v1/items - Liste des items
- POST /api/v1/items - Créer un item

## Authentification
L'API utilise JWT pour l'authentification (si configuré).

## Codes de réponse
- 200 - Succès
- 201 - Créé avec succès
- 400 - Erreur de validation
- 401 - Non autorisé
- 404 - Non trouvé
- 500 - Erreur serveur
