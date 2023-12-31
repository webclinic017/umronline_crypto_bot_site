from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from database import Database
from bybit_client import BybitClient
from log_module import CustomLogger
from common import *
from data_objects import *

app = Flask(__name__)

# Configure session to use PostgreSQL
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

db = Database()
db.connect()

logger = CustomLogger(LOG_FILE)

@app.route('/tv_webbhook/<username>', methods=['POST'])
def tv_webbhook(username):
    alert = request.get_data(as_text=True)
    logger.log('info', "#################### ALERT from tradingview: " + alert)
    side = alert.split(" ")[0]
    symbol = alert.split(" ")[1]
    user_settings = db.get_settings(username)
    bybit_client = BybitClient(user_settings.bybit_apikey, user_settings.bybit_secret)
    if(side.lower() == "buy"):
        account_usdt_before_buy = float(bybit_client.get_balance("USDT"))
        order_val_usdt = account_usdt_before_buy * ( float(user_settings.bybit_ordersize) / 100)
        order = bybit_client.place_market_buy_order(symbol, order_val_usdt)
        if(order != False):
            order.account_usdt_before_buy = account_usdt_before_buy
            order.username = username
            order.total_trading_fees = order.order_value * 0.001
            if(db.add_buy_order(order)):
                return "done"
            return
        else:
            return
    if (side.lower() == "sell"):
        account_usdt_before_sell = float(bybit_client.get_balance("USDT"))
        open_order = db.get_open_order(username, symbol, "bybit")
        if (open_order != False):
            quantity = open_order.buy_quantity
            available_quantity = float(bybit_client.get_balance(symbol.replace("USDT","")))
            if(available_quantity < quantity):
                quantity = available_quantity
            order = bybit_client.place_market_sell_order(symbol, quantity, open_order)
            if (order != False):
                order.id = open_order.id
                order.account_usdt_before_sell = account_usdt_before_sell
                account_usdt_after_sell = float(bybit_client.get_balance("USDT"))
                order.account_usdt_after_sell = account_usdt_after_sell
                order.total_trading_fees = order.order_value * 0.002
                order.profit = round(order.account_usdt_after_sell - order.account_usdt_before_buy ,5)
                order.profit_percentage = round((order.profit / order.account_usdt_before_buy) * 100, 5)
                if(db.update_sell_order(order)):
                    return "done"
                return
            else:
                return
        else:
            return


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'username' in session:
            username = session["username"]
            current_date = get_current_date()

            exchanges = []

            exchange_name = "bybit"
            exchange = Exchange()
            exchange.name = exchange_name
            user_settings = db.get_settings(username)
            exchange.status = user_settings.bybit_bot_status
            orders = db.get_all_orders_by_date_and_exchange(username, current_date, exchange_name)
            bybit_client = BybitClient(user_settings.bybit_apikey, user_settings.bybit_secret)
            exchange.current_balance = round(float(bybit_client.get_balance("USDT")),5)
            order_summary = get_summary_of_orders(orders)
            exchange.trades = order_summary["total_trades"]
            exchange.profit = order_summary["total_profit"]
            exchange.total_trading_fees = order_summary["total_trading_fees"]
            if(len(orders)>0):
                exchange.starting_balance = round(orders[0].account_usdt_before_buy,5)
                exchange.symbol = orders[0].symbol
                exchange.profit_percentage = round((exchange.profit / exchange.starting_balance) * 100, 5)
                exchange.current_quantity = float(bybit_client.get_balance(exchange.symbol.replace("USDT", "")))
            else:
                exchange.starting_balance = round(exchange.current_balance,5)
            exchanges.append(exchange)

            dashboard = {
                "date": get_current_date_beautified(),
                "time": get_current_time_beautified(),
                "today_target": get_today_target(user_settings),
                "target_achieved": exchange.profit_percentage,
                "total_profit": exchange.profit
            }
            try:
                logs = extract_logs_for_today()
            except Exception as e:
                logger.log('error', "dashboard page issue: " + str(e))
                logs = ""

            return render_template("dashboard.html", exchanges=exchanges, dashboard=dashboard, username=username, logs=logs)
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
            "BYBIT_BOT_STATUS": user_settings.bybit_bot_status,
            "STATUS": user_settings.bybit_bot_status
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

@app.route('/trades', methods=['GET', 'POST'])
def trades():
    if request.method == 'POST':
        date = request.form.get('date_input')
    elif request.method == 'GET':
        date = get_current_date()
    username = session["username"]
    user_settings = db.get_settings(username)
    orders = db.get_all_orders_by_date_and_exchange(username, date)
    for order in orders:
        order.entry_time = beautify_datetime(order.entry_time)
        order.exit_time = beautify_datetime(order.exit_time)
    order_summary = get_summary_of_orders(orders)
    total_profit = order_summary["total_profit"]
    if (len(orders) > 0):
        profit = round(total_profit,5)
        profit_percentage = round((profit / orders[0].account_usdt_before_buy) * 100,5)
    else:
        profit = 0
        profit_percentage = 0
    trades = {
        "date_raw": date,
        "date": beautify_date(date),
        "target": get_target(date, user_settings),
        "target_achieved": profit_percentage,
        "total_profit": profit
    }
    return render_template("trades.html",orders=orders, trades=trades)

if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(host='0.0.0.0', port=3100, debug=True)
