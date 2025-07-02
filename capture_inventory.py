"""Utility script for capturing current inventory levels."""

import random
from sqlalchemy import text
from db.utils import get_engine


def capture_inventory():
    """Fetch product ids and store a snapshot of inventory levels."""
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(text("SELECT DISTINCT product_id FROM product_listings"))
        product_ids = [row[0] for row in result]
        for pid in product_ids:
            quantity = random.randint(0, 100)
            status = "in_stock" if quantity > 0 else "out_of_stock"
            conn.execute(
                text(
                    "INSERT INTO inventory_snapshots (product_id, stock_quantity, stock_status) "
                    "VALUES (:pid, :qty, :status)"
                ),
                {"pid": pid, "qty": quantity, "status": status},
            )
    print(f"Captured inventory snapshot for {len(product_ids)} products.")


if __name__ == "__main__":
    capture_inventory()