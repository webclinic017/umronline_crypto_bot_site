DROP TABLE users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);
INSERT INTO users (username, password) VALUES ('umronline', 'youmronly');
INSERT INTO users (username, password) VALUES ('gg', 'gg');

DROP TABLE settings;
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    target_monday DECIMAL(10, 5),
    target_tuesday DECIMAL(10, 5),
    target_wednesday DECIMAL(10, 5),
    target_thursday DECIMAL(10, 5),
    target_friday DECIMAL(10, 5),
    target_saturday DECIMAL(10, 5),
    target_sunday DECIMAL(10, 5),
    bybit_stoploss DECIMAL(10, 5),
    bybit_ordersize DECIMAL(10, 5),
    bybit_apikey VARCHAR(200),
    bybit_secret VARCHAR(200),
    bybit_trading_type VARCHAR(20),
    bybit_bot_status VARCHAR(20)
);
INSERT INTO settings (username, target_monday, target_tuesday, target_wednesday, target_thursday, target_friday, target_saturday, target_sunday, bybit_stoploss, bybit_ordersize, bybit_apikey, bybit_secret, bybit_trading_type, bybit_bot_status)
VALUES ('gg', 1, 1, 1, 1, 1, 1, 1, 1, 50, 'G9egFxxxqtEVw3Lwjf', 'Lo8Ix1J0lIG3kKdc8psJkGaAsohePQkAVTjX', 'market', 'active');

DROP TABLE orders;
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    exchange VARCHAR(50) NOT NULL,
    status VARCHAR(50),
    order_value DECIMAL(30, 10),
    symbol VARCHAR(50),
    buy_quantity DECIMAL(30, 10),
    type VARCHAR(50),
    account_usdt_before_buy DECIMAL(30, 10),
    entry_time TIMESTAMP,
    buy_price DECIMAL(30, 10),
    account_usdt_before_sell DECIMAL(30, 10),
    exit_time TIMESTAMP,
    sell_price DECIMAL(30, 10),
    sell_quantity DECIMAL(30, 10),
    account_usdt_after_sell DECIMAL(30, 10),
    total_trading_fees DECIMAL(30, 10),
    profit_percentage DECIMAL(30, 10),
    profit DECIMAL(30, 10)
);