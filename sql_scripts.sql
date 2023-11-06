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
VALUES ('gg', 1, 1, 1, 1, 1, 1, 1, 1, 50, 'sHFo810ThZII4pfkJ1hcHrtRyHHdxuNLU2csTsuC6WgyamMimAqhM51DYV107oef', 'cUY9G1URmFEbGNXNM0YTU5sDQeAR1keyRvrlVw1RfvOgYRIyG5uSJpeaLRsgxf5v', 'market', 'active');