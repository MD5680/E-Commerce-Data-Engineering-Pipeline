import pandas as pd
from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Create processed folder if it does not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# 1. CLEAN CUSTOMERS
# =========================

customers = pd.read_csv(RAW_DIR / "customers_dataset.csv")

print("Customers before cleaning:")
print(customers.shape)


# Remove unnecessary spaces from text columns
customers["customer_id"] = customers["customer_id"].str.strip()
customers["customer_unique_id"] = customers["customer_unique_id"].str.strip()
customers["customer_city"] = customers["customer_city"].str.strip()
customers["customer_state"] = customers["customer_state"].str.strip()


# Convert city to lowercase for consistency
customers["customer_city"] = customers["customer_city"].str.lower()


# Convert state to uppercase for consistency
customers["customer_state"] = customers["customer_state"].str.upper()


# Convert ZIP code prefix to string
customers["customer_zip_code_prefix"] = (
    customers["customer_zip_code_prefix"]
    .astype(str)
    .str.strip()
)


# Remove duplicate rows
customers = customers.drop_duplicates()


# Save cleaned dataset
customers.to_csv(
    PROCESSED_DIR / "customers_cleaned.csv",
    index=False
)


print("Customers after cleaning:")
print(customers.shape)

print("\nCustomers cleaning completed successfully.")
print("Saved to:", PROCESSED_DIR / "customers_cleaned.csv")

# =========================
# 2. CLEAN ORDERS
# =========================

orders = pd.read_csv(RAW_DIR / "orders_dataset.csv")

print("\nOrders before cleaning:")
print(orders.shape)


# Remove unnecessary spaces from text columns
orders["order_id"] = orders["order_id"].str.strip()
orders["customer_id"] = orders["customer_id"].str.strip()
orders["order_status"] = orders["order_status"].str.strip().str.lower()


# Convert date columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        dayfirst=True,
        errors="coerce"
    )


# Remove duplicate rows
orders = orders.drop_duplicates()


# Save cleaned orders dataset
orders.to_csv(
    PROCESSED_DIR / "orders_cleaned.csv",
    index=False
)


print("Orders after cleaning:")
print(orders.shape)

print("\nOrders cleaning completed successfully.")
print("Saved to:", PROCESSED_DIR / "orders_cleaned.csv")

# =========================
# 3. CLEAN ORDER ITEMS
# =========================

order_items = pd.read_csv(
    RAW_DIR / "order_items_dataset.csv"
)

print("\nOrder Items before cleaning:")
print(order_items.shape)


# Remove unnecessary spaces from ID columns
order_items["order_id"] = order_items["order_id"].str.strip()
order_items["product_id"] = order_items["product_id"].str.strip()
order_items["seller_id"] = order_items["seller_id"].str.strip()


# Convert order_item_id to integer
order_items["order_item_id"] = pd.to_numeric(
    order_items["order_item_id"],
    errors="coerce"
)


# Convert shipping date to datetime
order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    dayfirst=True,
    errors="coerce"
)


# Convert price and freight value to numeric
order_items["price"] = pd.to_numeric(
    order_items["price"],
    errors="coerce"
)

order_items["freight_value"] = pd.to_numeric(
    order_items["freight_value"],
    errors="coerce"
)


# Remove duplicate rows
order_items = order_items.drop_duplicates()


# Save cleaned order items
order_items.to_csv(
    PROCESSED_DIR / "order_items_cleaned.csv",
    index=False
)


print("Order Items after cleaning:")
print(order_items.shape)

print("\nOrder Items cleaning completed successfully.")
print(
    "Saved to:",
    PROCESSED_DIR / "order_items_cleaned.csv"
)

# =========================
# 4. CLEAN PRODUCTS
# =========================

products = pd.read_csv(
    RAW_DIR / "products_dataset.csv"
)

print("\nProducts before cleaning:")
print(products.shape)


# Remove unnecessary spaces from product ID
products["product_id"] = products["product_id"].str.strip()


# Clean product category
products["product_category_name"] = (
    products["product_category_name"]
    .str.strip()
    .str.lower()
)


# Convert numeric columns to numeric type
numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in numeric_columns:
    products[column] = pd.to_numeric(
        products[column],
        errors="coerce"
    )


# Remove duplicate rows
products = products.drop_duplicates()


# Save cleaned products dataset
products.to_csv(
    PROCESSED_DIR / "products_cleaned.csv",
    index=False
)


print("Products after cleaning:")
print(products.shape)

print("\nProducts cleaning completed successfully.")
print(
    "Saved to:",
    PROCESSED_DIR / "products_cleaned.csv"
)