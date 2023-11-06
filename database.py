from data_objects import *
import psycopg2
import config

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
                setting.target_monday = setting_result[2]
                setting.target_tuesday = setting_result[3]
                setting.target_wednesday = setting_result[4]
                setting.target_thursday = setting_result[5]
                setting.target_friday = setting_result[6]
                setting.target_saturday = setting_result[7]
                setting.target_sunday = setting_result[8]
                setting.bybit_stoploss = setting_result[9]
                setting.bybit_ordersize = setting_result[10]
                setting.bybit_apikey = setting_result[11]
                setting.bybit_secret = setting_result[12]
                setting.bybit_trading_type = setting_result[13]
                setting.bybit_bot_status = setting_result[14]
        return setting

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