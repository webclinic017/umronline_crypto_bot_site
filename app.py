# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from config import *
from database import Database

app = Flask(__name__)

# Configure session to use PostgreSQL
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

db = Database()
db.connect()

@app.route('/')
def index():
    if 'username' in session:
        return f"Welcome, {session['username']}!<br><a href='/logout'>Logout</a>"
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(username)
        if user and user.password == password:
            session['username'] = user.username  # Store the username in the session
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/settings')
def settings():
    if 'username' in session:
        username = session["username"]
        user_settings = db.get_settings(username)
        user_target_settings = {
            TARGET_DAYS[0]: user_settings.target_monday,
            TARGET_DAYS[1]: user_settings.target_tuesday,
            TARGET_DAYS[2]: user_settings.target_wednesday,
            TARGET_DAYS[3]: user_settings.target_thursday,
            TARGET_DAYS[4]: user_settings.target_friday,
            TARGET_DAYS[5]: user_settings.target_saturday,
            TARGET_DAYS[6]: user_settings.target_sunday
        }
        bybit_config = {
            "API_KEY": user_settings.bybit_apikey,
            "SECRET": user_settings.bybit_secret,
            "STOP_LOSS": user_settings.bybit_stoploss,
            "ORDER_SIZE": user_settings.bybit_ordersize,
            "BYBIT_BOT_STATUS": user_settings.bybit_bot_status
        }
        return render_template("settings.html", user_target_settings=user_target_settings, target_days=TARGET_DAYS, target_values=TARGET_VALUES, bybit_config=bybit_config, stoploss_values=STOPLOSS_VALUES, ordersize_values=ORDERSIZE_VALUES)
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/update_targets', methods=['POST'])
def update_targets():
    targets = request.json
    username = session["username"]
    db.update_target_settings(username, targets)
    return "done"

@app.route('/update_bybit_settings', methods=['POST'])
def update_bybit_settings():
    bybit_settings = request.json
    username = session["username"]
    db.update_bybit_settings(username, bybit_settings)
    return "done"


if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(host='0.0.0.0', port=3100, debug=True)
