# ORACXPRED - Tournoi eFootball Mobile 2026 (Flask)

Ce projet est une petite application Flask pour afficher et administrer un bracket (8–16 joueurs) avec une coupe au centre, barres de progression et une page administrateur pour mettre à jour manuellement scores & résultats.

Fonctionnalités principales
- Page visualisateur (`/`) : lecture seule, bracket interactif, progression, responsive.
- Page administrateur (`/admin`) : accès protégé par mot de passe, modification du fichier `players.json`.
- Backend Flask qui lit/écrit `players.json`.
- Frontend en HTML/CSS/JS (style noir + doré).

Installation rapide
1. Créez un environnement virtuel et installez les dépendances :
   - python -m venv .venv
   - source .venv/bin/activate   (ou .venv\Scripts\activate sur Windows)
   - pip install -r requirements.txt

2. (Optionnel) Personnaliser le mot de passe administrateur et la clé secrète :
   - Create a `.env` file with:
     FLASK_ADMIN_PASS=VotreMotDePasseAdmin
     FLASK_SECRET_KEY=UneCleSecreteLongue

   Par défaut, le mot de passe admin est `oracxpred2026` — changez-le en production.

3. Lancer l'application :
   - python app.py
   - Ouvrir http://127.0.0.1:5000

Format du fichier players.json
- players: liste d'objets { id, name }
- rounds: liste de rounds; chaque round est une liste de matches
- match: { id, p1, p2, score1, score2, winner }
  - p1/p2 = player id ou null
  - winner = player id or null (admin peut le définir)

Procédure d'administration
- Aller sur /admin
- Saisir le mot de passe
- L'interface admin permet de voir les données actuelles, modifier noms, scores, et sauvegarder
- Les visualisateurs verront les changements automatiquement (rafraîchissement en arrière-plan toutes les 2s)

Notes de sécurité & limites
- Authentification simple par session & mot de passe stocké en clair (ou via .env). Pour production, utiliser OAuth/SSO, HTTPS, et une gestion des utilisateurs.
- Les updates remplacent le JSON complet — l'admin UI envoie le JSON modifié. On peut l'étendre pour des endpoints plus granulaires.
- Polling client toutes les 2s pour refléter les changements en temps réel — remplacer par WebSocket/SSE si nécessaire pour grande échelle.

Exemples & customisation
- Pour étendre à 16 joueurs, ajustez `players` et `rounds` (4 rounds : 16->8->4->2->1).
- Le frontend calcule les barres de progression (ratio des scores dans le match) et affiche le gagnant si présent.

Si vous voulez, je peux :
- ajouter WebSocket/SSE pour push en temps réel,
- ajouter validation plus stricte côté serveur,
- générer un command-line script pour construire automatiquement la structure pour N joueurs.