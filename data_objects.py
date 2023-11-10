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

class Order:
    def __init__(self):
        self.id = ""
        self.username = ""
        self.exchange = ""
        self.status = ""
        self.order_value = 0
        self.symbol = ""
        self.buy_quantity = 0
        self.type = ""
        self.account_usdt_before_buy = 0
        self.entry_time = None
        self.buy_price = 0
        self.account_usdt_before_sell = 0
        self.exit_time = None
        self.sell_price = 0
        self.sell_quantity = 0
        self.account_usdt_after_sell = 0
        self.total_trading_fees = 0
        self.profit_percentage = 0
        self.profit = 0

class Exchange:
    def __init__(self):
        self.name = ""
        self.status = ""
        self.symbol = ""
        self.starting_balance = 0
        self.current_quantity = 0
        self.current_balance = 0
        self.trades = 0
        self.total_trading_fees = 0
        self.profit_percentage = 0
        self.profit = 0
