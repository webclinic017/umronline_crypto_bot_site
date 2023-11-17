# config.py

DATABASE_CONFIG = {
    'database': 'umronline_db',
    'user': 'umronline',
    'password': 'youmronly',
    'host': 'localhost',
    'port': '5432',
}

SECRET_KEY = 'secret_key_for_umronline_flask_app'

TARGET_DAYS = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
TARGET_VALUES = [ 0, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5 ]
STOPLOSS_VALUES = [0.25, 0.5, 0.75, 1, 1.25, 1.5]
ORDERSIZE_VALUES = [25, 50, 75, 100]

LOG_FILE = "app.log"
LOG_LEVEL = "INFO"

TIMEZONE_OFFSET_STR = '+4:00'