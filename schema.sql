CREATE TABLE categories (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL UNIQUE
);
CREATE TABLE products (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
price REAL NOT NULL,
category_id INTEGER,
FOREIGN KEY (category_id) REFERENCES categories(id)
);
CREATE INDEX idx_products_name ON products(name);
