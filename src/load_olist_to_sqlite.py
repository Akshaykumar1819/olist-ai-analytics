import pandas as pd
import sqlite3
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = PROCESSED_DIR / "olist.db"

# Create processed directory if not exists
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("Loading CSV files...")

# Load datasets
orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
order_items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")
geolocation = pd.read_csv(RAW_DIR / "olist_geolocation_dataset.csv")
translation = pd.read_csv(RAW_DIR / "product_category_name_translation.csv")

print(f"Loaded orders: {len(orders)} rows")
print(f"Loaded order_items: {len(order_items)} rows")
print(f"Loaded customers: {len(customers)} rows")
print(f"Loaded sellers: {len(sellers)} rows")
print(f"Loaded products: {len(products)} rows")
print(f"Loaded reviews: {len(reviews)} rows")
print(f"Loaded payments: {len(payments)} rows")
print(f"Loaded geolocation: {len(geolocation)} rows")
print(f"Loaded category_translation: {len(translation)} rows")

print("\nConnecting to SQLite database...")

# SQLite connection
conn = sqlite3.connect(DB_PATH)

# Save raw tables
orders.to_sql("orders", conn, if_exists="replace", index=False)
customers.to_sql("customers", conn, if_exists="replace", index=False)
order_items.to_sql("order_items", conn, if_exists="replace", index=False)
payments.to_sql("payments", conn, if_exists="replace", index=False)
reviews.to_sql("reviews", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
sellers.to_sql("sellers", conn, if_exists="replace", index=False)
geolocation.to_sql("geolocation", conn, if_exists="replace", index=False)
translation.to_sql("category_translation", conn, if_exists="replace", index=False)

print("\nBuilding fact table...")

# Build fact table
fact_order_items = order_items.merge(
    orders,
    on="order_id",
    how="left"
)

fact_order_items.to_sql(
    "fact_order_items",
    conn,
    if_exists="replace",
    index=False
)

print(f"fact_order_items: {len(fact_order_items)} rows")

print("\nBuilding dimension tables...")

# Dimension tables
customers.to_sql("dim_customer", conn, if_exists="replace", index=False)
sellers.to_sql("dim_seller", conn, if_exists="replace", index=False)
products.to_sql("dim_product", conn, if_exists="replace", index=False)

print(f"dim_customer: {len(customers)} rows")
print(f"dim_seller: {len(sellers)} rows")
print(f"dim_product: {len(products)} rows")

conn.close()

print(f"\nDatabase written to:\n{DB_PATH}")
print("\nDone.")