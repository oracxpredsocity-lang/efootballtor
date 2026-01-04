from flask import Flask, render_template, jsonify, request, redirect, url_for, session, abort
import os
import json
import threading
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_ROOT, 'players.json')
ADMIN_PASS = os.getenv('FLASK_ADMIN_PASS', 'oracxpred2026')  # change in production!
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'change_this_secret_key')

lock = threading.Lock()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = SECRET_KEY


def load_data():
    with lock:
        if not os.path.exists(DATA_FILE):
            return {"players": [], "rounds": []}
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)


def save_data(data):
    with lock:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return abort(403)
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # simple login form
    if request.method == 'POST':
        pw = request.form.get('password', '')
        if pw == ADMIN_PASS:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin.html', error='Mot de passe incorrect')
    if not session.get('is_admin'):
        return render_template('admin.html')
    return render_template('admin.html', authenticated=True)


# API route to get current data (public)
@app.route('/api/data', methods=['GET'])
def api_data():
    data = load_data()
    return jsonify(data)


# API route to update entire data file (admin only)
@app.route('/api/update', methods=['POST'])
@admin_required
def api_update():
    try:
        new_data = request.get_json()
        if not isinstance(new_data, dict):
            return jsonify({"error": "Invalid payload"}), 400
        # basic validation (ensure players and rounds keys exist)
        if 'players' not in new_data or 'rounds' not in new_data:
            return jsonify({"error": "Payload must contain 'players' and 'rounds'"}), 400
        save_data(new_data)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Admin logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin'))


if __name__ == '__main__':
    # ensure there's an example players.json if missing
    if not os.path.exists(DATA_FILE):
        example = {
            "players": [
                {"id": 1, "name": "Player A"},
                {"id": 2, "name": "Player B"},
                {"id": 3, "name": "Player C"},
                {"id": 4, "name": "Player D"},
                {"id": 5, "name": "Player E"},
                {"id": 6, "name": "Player F"},
                {"id": 7, "name": "Player G"},
                {"id": 8, "name": "Player H"}
            ],
            # rounds: array of rounds; each round is list of matches.
            # match: { "id": "<r>-<m>", "p1": player_id or null, "p2": player_id or null, "score1": int, "score2": int, "winner": player_id or null }
            "rounds": [
                [  # Round 0 (quarterfinals for 8 players)
                    {"id": "r0-m0", "p1": 1, "p2": 8, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r0-m1", "p1": 4, "p2": 5, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r0-m2", "p1": 2, "p2": 7, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r0-m3", "p1": 3, "p2": 6, "score1": 0, "score2": 0, "winner": None}
                ],
                [  # Round 1 (semifinals)
                    {"id": "r1-m0", "p1": None, "p2": None, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r1-m1", "p1": None, "p2": None, "score1": 0, "score2": 0, "winner": None}
                ],
                [  # Round 2 (final)
                    {"id": "r2-m0", "p1": None, "p2": None, "score1": 0, "score2": 0, "winner": None}
                ]
            ]
        }
        save_data(example)
        print("Created example players.json")
    app.run(host='0.0.0.0', port=5000, debug=True)