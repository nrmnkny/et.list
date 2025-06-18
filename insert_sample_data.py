# insert_sample_data.py

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from config import DB_SETTINGS

def get_engine():
    encoded_password = quote_plus(DB_SETTINGS['password'])
    url = f"postgresql://{DB_SETTINGS['user']}:{encoded_password}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['database']}"
    return create_engine(url, echo=True)

def insert_sample_store_locations():
    data = [
        {
            "name": "BestBuy Downtown",
            "address": "123 Main St, Cityville",
            "latitude": 38.8951,
            "longitude": -77.0364,
            "category": "Electronics"
        },
        {
            "name": "Target Express",
            "address": "456 Elm St, Townburg",
            "latitude": 38.8895,
            "longitude": -77.0352,
            "category": "Retail"
        }
    ]

    engine = get_engine()
    with engine.begin() as conn:
        print("👉 Inserting:", data)
        conn.execute(
            text("""
                INSERT INTO store_locations (name, address, latitude, longitude, category)
                VALUES (:name, :address, :latitude, :longitude, :category)
            """),
            data
        )

    print("✅ Sample store locations inserted!")

if __name__ == "__main__":
    insert_sample_store_locations()
