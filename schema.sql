CREATE TABLE IF NOT EXISTS locations (
    pin_code VARCHAR(10) PRIMARY KEY,
    state VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(30) PRIMARY KEY,
    order_date DATE NOT NULL,
    product VARCHAR(150) NOT NULL,
    state VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    pin_code VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    revenue DECIMAL(14,2) NOT NULL,
    platform VARCHAR(80),
    FOREIGN KEY (pin_code) REFERENCES locations(pin_code)
);

CREATE INDEX idx_orders_state ON orders(state);
CREATE INDEX idx_orders_city ON orders(city);
CREATE INDEX idx_orders_pin ON orders(pin_code);
CREATE INDEX idx_orders_date ON orders(order_date);
