# insert_mock_products.py

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from config import DB_SETTINGS

def get_engine():
    password = quote_plus(DB_SETTINGS['password'])
    url = f"postgresql://{DB_SETTINGS['user']}:{password}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['database']}"
    return create_engine(url)

def insert_mock_products():
    data = [
        {
            "product_id": "P001",
            "title": "Wireless Earbuds",
            "price": 49.99,
            "currency": "USD",
            "category": "Electronics",
            "vendor": "AudioMax",
            "product_url": "http://example.com/earbuds"
        },
        {
            "product_id": "P002",
            "title": "Portable Blender",
            "price": 29.99,
            "currency": "USD",
            "category": "Kitchen",
            "vendor": "BlendPro",
            "product_url": "http://example.com/blender"
        },
        {
            "product_id": "P003",
            "title": "Smart Watch",
            "price": 99.99,
            "currency": "USD",
            "category": "Wearables",
            "vendor": "WristTech",
            "product_url": "http://example.com/smartwatch"
        },
        {
            "product_id": "P004",
            "title": "Electric Kettle",
            "price": 24.99,
            "currency": "USD",
            "category": "Kitchen",
            "vendor": "HeatEase",
            "product_url": "http://example.com/kettle"
        },
        {
            "product_id": "P005",
            "title": "Noise Cancelling Headphones",
            "price": 149.99,
            "currency": "USD",
            "category": "Electronics",
            "vendor": "AudioMax",
            "product_url": "http://example.com/headphones"
        }
    ]

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO product_listings (
                    product_id, title, price, currency, category, vendor, product_url
                ) VALUES (
                    :product_id, :title, :price, :currency, :category, :vendor, :product_url
                )
            """),
            data
        )

    print("✅ Mock product listings inserted!")

if __name__ == "__main__":
    insert_mock_products()
