# ORACXPRED - Tournoi eFootball Mobile 2026 (Flask)

Contenu du projet
- app.py : application Flask (routes publiques et admin)
- players.json : données du tournoi (joueurs + rounds)
- templates/ : pages HTML (index, admin)
- static/ : CSS / JS / assets
- .env.example : variables d'environnement (admin password/token, secret)
- requirements.txt : dépendances
- .gitignore

Installation rapide
1. Créer un environnement virtuel et installer les dépendances
   - python -m venv .venv
   - source .venv/bin/activate  (Windows: .venv\\Scripts\\activate)
   - pip install -r requirements.txt

2. Copier `.env.example` en `.env` et adapter :
   - FLASK_ADMIN_PASS : mot de passe admin (optionnel si vous utilisez token)
   - FLASK_ADMIN_TOKEN : (optionnel) token long non-guessable pour connexion via /admin?token=...
   - FLASK_SECRET_KEY : clé secrète pour les sessions Flask

3. Lancer l'application
   - python app.py
   - Ouvrir http://127.0.0.1:5000 pour visualiser le bracket
   - Admin : http://127.0.0.1:5000/admin (ou /admin?token=VOTRE_TOKEN)

Format du fichier players.json
- players: liste d'objets { id (int), name (string), controller (string), team (string) }
- rounds: liste de rounds; chaque round est une liste de matches
- match: { id (string), p1 (player id|null), p2 (player id|null), score1 (int), score2 (int), winner (player id|null) }

Administration
- Se connecter via formulaire (mot de passe) ou via token dans l'URL.
- Page admin permet d'éditer le JSON complet et sauvegarder.
- Les visualisateurs rechargent automatiquement les données toutes les 2s (polling).

Sécurité & recommandations
- Changez FLASK_ADMIN_PASS et/ou FLASK_ADMIN_TOKEN dans .env. N'utilisez pas les valeurs par défaut en production.
- Activez HTTPS derrière un reverse-proxy (nginx) en production.
- Pour une solution multi-admin ou plus sécurisée, utilisez Flask-Login + stockage des comptes (hash des mots de passe) ou OAuth/SSO.

Extensions possibles
- Remplacer le polling par SSE / WebSocket pour push en temps réel.
- UI admin par match (formulaire) au lieu d'éditer JSON brut.
- Générateur automatique des rounds pour 8/16 joueurs.
- Sauvegarde/backup du players.json avec historisation avant chaque changement.

Si vous voulez que je génère automatiquement :
- Dockerfile + docker-compose,
- endpoint plus granulaire / UI admin par match,
- script pour construire rounds automatiquement pour N joueurs,
dites-moi ce que vous préférez et je l'ajoute.
