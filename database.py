from data_objects import *
import psycopg2
import config
from log_module import CustomLogger

logger = CustomLogger("app.log")

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(**config.DATABASE_CONFIG)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def create_user(self, username, password):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

    def get_user(self, username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user_result = cursor.fetchone()
                user = User()
                user.id = user_result[0]
                user.username = user_result[1]
                user.password = user_result[2]
        return user

    def get_settings(self, username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM settings WHERE username = %s", (username,))
                setting_result = cursor.fetchone()
                setting = Setting()
                setting.id = setting_result[0]
                setting.username = setting_result[1]
                setting.target_monday = self.make_float(setting_result[2])
                setting.target_tuesday = self.make_float(setting_result[3])
                setting.target_wednesday = self.make_float(setting_result[4])
                setting.target_thursday = self.make_float(setting_result[5])
                setting.target_friday = self.make_float(setting_result[6])
                setting.target_saturday = self.make_float(setting_result[7])
                setting.target_sunday = self.make_float(setting_result[8])
                setting.bybit_stoploss = self.make_float(setting_result[9])
                setting.bybit_ordersize = self.make_float(setting_result[10])
                setting.bybit_apikey = setting_result[11]
                setting.bybit_secret = setting_result[12]
                setting.bybit_trading_type = setting_result[13]
                setting.bybit_bot_status = setting_result[14]
        return setting

    def make_float(self, val):
        try:
            return float(val)
        except:
            return 0

    def update_target_settings(self, username, targets):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE settings SET target_monday = %s, target_tuesday = %s, target_wednesday = %s, target_thursday = %s, target_friday = %s, target_saturday = %s, target_sunday = %s WHERE username = %s",
                               (float(targets["Monday"]), float(targets["Tuesday"]), float(targets["Wednesday"]), float(targets["Thursday"]), float(targets["Friday"]), float(targets["Saturday"]), float(targets["Sunday"]), username, ))
        self.connection.commit()
        return True

    def update_bybit_settings(self, username, bybit_settings):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE settings SET bybit_stoploss = %s, bybit_ordersize = %s, bybit_apikey = %s, bybit_secret = %s WHERE username = %s",
                               (float(bybit_settings["stop_loss"]), float(bybit_settings["order_size"]), bybit_settings["api_key"], bybit_settings["secret"], username, ))
        self.connection.commit()
        return True

    def add_buy_order(self, order):
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO orders (username, exchange, status, order_value, symbol, buy_quantity, type, account_usdt_before_buy, entry_time, buy_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                   (order.username, order.exchange, order.status, order.order_value, order.symbol, order.buy_quantity, order.type, order.account_usdt_before_buy, order.entry_time, order.buy_price))
            return True
        except Exception as e:
            logger.log('error', "db error - add_buy_order: " + str(e))
            return False

    def update_sell_order(self, order):
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("UPDATE orders SET account_usdt_before_sell = %s, exit_time = %s, sell_price = %s, sell_quantity = %s, account_usdt_after_sell = %s, total_trading_fees = %s, profit_percentage = %s, profit = %s WHERE id = %s",
                                   (order.account_usdt_before_sell, order.exit_time, order.sell_price, order.sell_quantity, order.account_usdt_after_sell, order.total_trading_fees, order.profit_percentage, order.profit, order.id))
            return True
        except Exception as e:
            logger.log('error', "db error - update_sell_order: " + str(e))
            return False

    def get_open_order(self, username, symbol, exchange):
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM orders WHERE username = %s AND symbol = %s AND exchange = %s AND status = 'bought' ORDER BY entry_time DESC LIMIT 1",
                                   (username, symbol, exchange))
                    order_result = cursor.fetchone()
                    order = Order()
                    order.id = order_result[0]
                    order.username = order_result[1]
                    order.exchange = order_result[2]
                    order.status = order_result[3]
                    order.order_value = self.make_float(order_result[4])
                    order.symbol = order_result[5]
                    order.buy_quantity = self.make_float(order_result[6])
                    order.type = order_result[7]
                    order.account_usdt_before_buy = self.make_float(order_result[8])
                    order.entry_time = order_result[9]
                    order.buy_price = self.make_float(order_result[10])
                    return order
        except Exception as e:
            logger.log('error', "db error - get_open_order: " + str(e))
            return False