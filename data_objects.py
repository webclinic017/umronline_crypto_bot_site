class User:
    def __init__(self):
        self.id = ""
        self.username = ""
        self.password = ""

class Setting:
    def __init__(self):
        self.id = ""
        self.username = ""
        self.target_monday = 0
        self.target_tuesday = 0
        self.target_wednesday = 0
        self.target_thursday = 0
        self.target_friday = 0
        self.target_saturday = 0
        self.target_sunday = 0
        self.bybit_stoploss = 0
        self.bybit_ordersize = 0
        self.bybit_apikey = ""
        self.bybit_secret = ""
        self.bybit_trading_type = ""
        self.bybit_bot_status = ""