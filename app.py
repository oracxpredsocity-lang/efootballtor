import os
import json
import threading
from functools import wraps
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, abort
from dotenv import load_dotenv

load_dotenv()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_ROOT, 'players.json')

# Auth / session settings
ADMIN_PASS = os.getenv('FLASK_ADMIN_PASS', 'oracxpred2026')
ADMIN_TOKEN = os.getenv('FLASK_ADMIN_TOKEN', None)
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
    # login via ?token=TOKEN
    token = request.args.get('token')
    if token and ADMIN_TOKEN and token == ADMIN_TOKEN:
        session['is_admin'] = True
        return redirect(url_for('admin'))

    # login via form (password)
    if request.method == 'POST':
        pw = request.form.get('password', '')
        if pw == ADMIN_PASS:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin.html', error='Mot de passe incorrect')

    # If not authenticated, show login form
    if not session.get('is_admin'):
        return render_template('admin.html')

    # Authenticated admin: show dashboard
    return render_template('admin.html', authenticated=True)


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin'))


# Public API: get tournament data
@app.route('/api/data', methods=['GET'])
def api_data():
    data = load_data()
    return jsonify(data)


# Admin API: replace entire data (must send full JSON with players + rounds)
@app.route('/api/update', methods=['POST'])
@admin_required
def api_update():
    try:
        new_data = request.get_json()
        if not isinstance(new_data, dict):
            return jsonify({"error": "Invalid payload"}), 400
        if 'players' not in new_data or 'rounds' not in new_data:
            return jsonify({"error": "Payload must contain 'players' and 'rounds'"}), 400
        save_data(new_data)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Optional: admin can update a single match (PUT) - convenience endpoint
@app.route('/api/match/<match_id>', methods=['PUT'])
@admin_required
def api_update_match(match_id):
    """
    Payload: { "score1": int, "score2": int, "winner": player_id or null }
    This will search through rounds and matches to update the match with id == match_id.
    """
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "No payload"}), 400
    data = load_data()
    updated = False
    for rnd in data.get('rounds', []):
        for m in rnd:
            if m.get('id') == match_id:
                # update allowed fields
                for field in ('score1', 'score2', 'winner', 'p1', 'p2'):
                    if field in payload:
                        m[field] = payload[field]
                updated = True
                break
        if updated:
            break
    if not updated:
        return jsonify({"error": "Match not found"}), 404
    save_data(data)
    return jsonify({"status": "ok", "match_id": match_id})


if __name__ == '__main__':
    # create example data if missing
    if not os.path.exists(DATA_FILE):
        example = {
            "players": [
                {"id": 1, "name": "Player A", "controller": "Théo", "team": "FC Oracx"},
                {"id": 2, "name": "Player B", "controller": "Lina", "team": "Golden Strikers"},
                {"id": 3, "name": "Player C", "controller": "Sam", "team": "Neo United"},
                {"id": 4, "name": "Player D", "controller": "Maya", "team": "Dark Wings"},
                {"id": 5, "name": "Player E", "controller": "Yann", "team": "Solar FC"},
                {"id": 6, "name": "Player F", "controller": "Rita", "team": "Volt Club"},
                {"id": 7, "name": "Player G", "controller": "Noa", "team": "Titanes"},
                {"id": 8, "name": "Player H", "controller": "Alex", "team": "Phantom XI"}
            ],
            "rounds": [
                [
                    {"id": "r0-m0", "p1": 1, "p2": 8, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r0-m1", "p1": 4, "p2": 5, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r0-m2", "p1": 2, "p2": 7, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r0-m3", "p1": 3, "p2": 6, "score1": 0, "score2": 0, "winner": None}
                ],
                [
                    {"id": "r1-m0", "p1": None, "p2": None, "score1": 0, "score2": 0, "winner": None},
                    {"id": "r1-m1", "p1": None, "p2": None, "score1": 0, "score2": 0, "winner": None}
                ],
                [
                    {"id": "r2-m0", "p1": None, "p2": None, "score1": 0, "score2": 0, "winner": None}
                ]
            ]
        }
        save_data(example)
        print("Created example players.json")
    app.run(host='0.0.0.0', port=5000, debug=True)
