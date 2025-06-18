# run_schema.py
from sqlalchemy import create_engine, text
from config import DB_SETTINGS
from urllib.parse import quote_plus

def run_schema():
    encoded_pw = quote_plus(DB_SETTINGS['password'])
    url = f"postgresql://{DB_SETTINGS['user']}:{encoded_pw}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['database']}"
    engine = create_engine(url)

    with open("db/schema.sql", "r") as f:
        sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql))
        print("✅ Tables created on Render!")

if __name__ == "__main__":
    run_schema()
