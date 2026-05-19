import sqlite3
from pathlib import Path
import pandas as pd

# Database path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "olist.db"

print("Connecting to warehouse...\n")

conn = sqlite3.connect(DB_PATH)

queries = {
    "Orders Count":
        "SELECT COUNT(*) AS total_orders FROM orders",

    "Customers Count":
        "SELECT COUNT(*) AS total_customers FROM customers",

    "Products Count":
        "SELECT COUNT(*) AS total_products FROM products",

    "Fact Table Count":
        "SELECT COUNT(*) AS total_fact_rows FROM fact_order_items",

    "Top 5 Product Categories":
        """
        SELECT product_category_name,
               COUNT(*) AS total
        FROM products
        GROUP BY product_category_name
        ORDER BY total DESC
        LIMIT 5
        """
}

for title, query in queries.items():
    print(f"=== {title} ===")
    result = pd.read_sql_query(query, conn)
    print(result)
    print("\n")

conn.close()

print("Warehouse verification completed successfully.")