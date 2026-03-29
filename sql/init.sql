-- ============================================================
-- PO Management System - PostgreSQL Schema
-- ============================================================

-- VENDORS table
CREATE TABLE IF NOT EXISTS vendors (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    contact     VARCHAR(255) NOT NULL,
    rating      NUMERIC(2, 1) CHECK (rating >= 0 AND rating <= 5),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PRODUCTS table
CREATE TABLE IF NOT EXISTS products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    sku         VARCHAR(100) UNIQUE NOT NULL,
    unit_price  NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    stock_level INTEGER NOT NULL DEFAULT 0 CHECK (stock_level >= 0),
    category    VARCHAR(100),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PURCHASE ORDERS table
CREATE TABLE IF NOT EXISTS purchase_orders (
    id           SERIAL PRIMARY KEY,
    reference_no VARCHAR(50) UNIQUE NOT NULL,
    vendor_id    INTEGER NOT NULL REFERENCES vendors(id) ON DELETE RESTRICT,
    subtotal     NUMERIC(10, 2) NOT NULL DEFAULT 0,
    tax_amount   NUMERIC(10, 2) NOT NULL DEFAULT 0,   -- 5% tax
    total_amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
    status       VARCHAR(50) NOT NULL DEFAULT 'Draft'
                 CHECK (status IN ('Draft', 'Confirmed', 'Received', 'Cancelled')),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PO ITEMS table (line items inside a PO)
CREATE TABLE IF NOT EXISTS po_items (
    id          SERIAL PRIMARY KEY,
    po_id       INTEGER NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
    product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10, 2) NOT NULL,   -- snapshot of price at time of order
    line_total  NUMERIC(10, 2) NOT NULL    -- quantity * unit_price
);

-- ============================================================
-- Seed Data (for testing)
-- ============================================================

INSERT INTO vendors (name, contact, rating) VALUES
    ('TechSupply Co.',   'techsupply@email.com',  4.5),
    ('Global Parts Ltd', 'global@parts.com',      3.8),
    ('FastShip Inc.',    'fastship@logistics.com', 4.2)
ON CONFLICT DO NOTHING;

INSERT INTO products (name, sku, unit_price, stock_level, category) VALUES
    ('Wireless Keyboard',  'SKU-WK001', 29.99,  150, 'Electronics'),
    ('USB-C Hub 7-Port',   'SKU-UH002', 45.00,  80,  'Electronics'),
    ('Ergonomic Mouse',    'SKU-EM003', 34.50,  200, 'Electronics'),
    ('Office Chair',       'SKU-OC004', 199.99, 30,  'Furniture'),
    ('Standing Desk',      'SKU-SD005', 349.00, 15,  'Furniture')
ON CONFLICT DO NOTHING;