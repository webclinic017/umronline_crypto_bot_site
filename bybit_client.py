from pybit.unified_trading import HTTP
from log_module import CustomLogger
from data_objects import *
from common import *
import math

logger = CustomLogger("app.log")
class BybitClient:
    def __init__(self, BYBIT_API_KEY, BYBIT_SECRET_KEY):
        self.client = HTTP(testnet=False, api_key=BYBIT_API_KEY, api_secret=BYBIT_SECRET_KEY)

    def place_market_buy_order(self, symbol, quantity):
        try:
            quantity = round(quantity, 2)
            order_res = self.client.place_order(category="spot", symbol=symbol, side="BUY", orderType="Market", qty=str(quantity))
            logger.log('info', "Bybit market buy order successfully placed:")
            order_id = order_res["result"]["orderId"]
            executed_order = self.client.get_order_history(category="spot", orderId=order_id)
            logger.log('info', executed_order)
            order = Order()
            order.entry_time = get_current_datetime()
            order.exchange = "bybit"
            order.symbol = symbol
            order.buy_quantity = float(executed_order["result"]["list"][0]["cumExecQty"])
            order.order_value = float(executed_order["result"]["list"][0]["qty"])
            order.buy_price = float(executed_order["result"]["list"][0]["avgPrice"])
            order.type = "market"
            order.status = "bought"
            return order
        except Exception as e:
            logger.log('error', "Bybit error: " + str(e))
            return False

    def precise_quantity_bybit(self, coin, quantity):
        instrument_info = self.client.get_instruments_info(category="spot", symbol=coin)
        base_precision = float(instrument_info["result"]["list"][0]["lotSizeFilter"]["basePrecision"])
        print("base_precision: " + str(base_precision))
        truncate_num = math.log10(1 / base_precision)
        quantity = math.floor((quantity) * 10 ** truncate_num) / 10 ** truncate_num
        print("valid_quantity: " + str(quantity))
        return quantity

    def place_market_sell_order(self, symbol, quantity, order):
        try:
            quantity = self.precise_quantity_bybit(symbol, quantity)
            order_res = self.client.place_order(category="spot", symbol=symbol, side="SELL", orderType="Market", qty=str(quantity))
            logger.log('info', "Bybit market sell order successfully placed:")
            order_id = order_res["result"]["orderId"]
            executed_order = self.client.get_order_history(category="spot", orderId=order_id)
            logger.log('info', executed_order)
            order.exit_time = get_current_datetime()
            order.exchange = "bybit"
            order.symbol = symbol
            order.sell_price = float(executed_order["result"]["list"][0]["avgPrice"])
            order.sell_quantity = float(executed_order["result"]["list"][0]["qty"])
            order.type = "market"
            order.status = "sold"
            return order
        except Exception as e:
            logger.log('error', "Bybit error: " + str(e))
            return False

    def get_balance(self, coin):
        balance = self.client.get_wallet_balance(accountType="spot", coin=coin)
        coin_amount = float(balance["result"]["list"][0]["coin"][0]["free"])
        return coin_amount