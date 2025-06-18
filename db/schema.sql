CREATE TABLE IF NOT EXISTS store_locations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    category TEXT,
    source TEXT DEFAULT 'Google Maps',
    extracted_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS search_trends (
    id SERIAL PRIMARY KEY,
    keyword TEXT NOT NULL,
    region TEXT,
    interest_score INT,
    date DATE,
    source TEXT DEFAULT 'Google Trends',
    extracted_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS product_listings (
    id SERIAL PRIMARY KEY,
    product_id TEXT NOT NULL,
    title TEXT,
    price NUMERIC(10, 2),
    currency TEXT,
    category TEXT,
    vendor TEXT,
    product_url TEXT,
    source TEXT DEFAULT 'Shopify API',
    extracted_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS inventory_snapshots (
    id SERIAL PRIMARY KEY,
    product_id TEXT,
    stock_quantity INT,
    stock_status TEXT,
    captured_at TIMESTAMP DEFAULT NOW()
);
