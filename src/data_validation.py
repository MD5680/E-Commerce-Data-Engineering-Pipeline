import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"


# --------------------------------------------------
# Load customers dataset
# --------------------------------------------------

customers_file = DATA_DIR / "customers_dataset.csv"

customers = pd.read_csv(customers_file)


# --------------------------------------------------
# Customer data validation
# --------------------------------------------------

print("=" * 70)
print("CUSTOMER DATA VALIDATION")
print("=" * 70)


# 1. Check missing customer IDs

missing_customer_id = customers["customer_id"].isnull().sum()

print(f"\nMissing customer_id: {missing_customer_id}")


# 2. Check missing customer unique IDs

missing_unique_id = customers["customer_unique_id"].isnull().sum()

print(f"Missing customer_unique_id: {missing_unique_id}")


# 3. Check duplicate customer IDs

duplicate_customer_id = customers["customer_id"].duplicated().sum()

print(f"Duplicate customer_id: {duplicate_customer_id}")


# 4. Check completely duplicate rows

duplicate_rows = customers.duplicated().sum()

print(f"Duplicate rows: {duplicate_rows}")


# 5. Display validation result

if (
    missing_customer_id == 0
    and missing_unique_id == 0
    and duplicate_customer_id == 0
    and duplicate_rows == 0
):
    print("\nCustomer dataset validation: PASSED")
else:
    print("\nCustomer dataset validation: FAILED")


# --------------------------------------------------
# Load orders dataset
# --------------------------------------------------

orders_file = DATA_DIR / "orders_dataset.csv"

orders = pd.read_csv(orders_file)


# --------------------------------------------------
# Orders data validation
# --------------------------------------------------

print("\n" + "=" * 70)
print("ORDER DATA VALIDATION")
print("=" * 70)


# 1. Check missing order IDs

missing_order_id = orders["order_id"].isnull().sum()

print(f"\nMissing order_id: {missing_order_id}")


# 2. Check duplicate order IDs

duplicate_order_id = orders["order_id"].duplicated().sum()

print(f"Duplicate order_id: {duplicate_order_id}")


# 3. Check missing customer IDs

missing_order_customer_id = orders["customer_id"].isnull().sum()

print(f"Missing customer_id: {missing_order_customer_id}")


# 4. Check whether customer IDs exist in customer dataset

invalid_customer_ids = ~orders["customer_id"].isin(customers["customer_id"])

invalid_customer_count = invalid_customer_ids.sum()

print(f"Customer IDs not found in customers dataset: {invalid_customer_count}")


# 5. Check order status values

valid_statuses = [
    "delivered",
    "shipped",
    "canceled",
    "unavailable",
    "invoiced",
    "processing",
    "created",
    "approved"
]

invalid_status = ~orders["order_status"].isin(valid_statuses)

invalid_status_count = invalid_status.sum()

print(f"Invalid order_status values: {invalid_status_count}")


# 6. Check missing order purchase timestamps

missing_purchase_date = orders["order_purchase_timestamp"].isnull().sum()

print(f"Missing order_purchase_timestamp: {missing_purchase_date}")


# 7. Convert purchase timestamp to datetime

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    dayfirst=True,
    errors="coerce"
)


# 8. Check invalid purchase dates

invalid_purchase_date = orders["order_purchase_timestamp"].isnull().sum()

print(f"Invalid order_purchase_timestamp: {invalid_purchase_date}")


# --------------------------------------------------
# Final validation result
# --------------------------------------------------

if (
    missing_order_id == 0
    and duplicate_order_id == 0
    and missing_order_customer_id == 0
    and invalid_customer_count == 0
    and invalid_status_count == 0
    and invalid_purchase_date == 0
):
    print("\nOrder dataset validation: PASSED")
else:
    print("\nOrder dataset validation: REVIEW REQUIRED")

# --------------------------------------------------
# Load order items dataset
# --------------------------------------------------

order_items_file = DATA_DIR / "order_items_dataset.csv"

order_items = pd.read_csv(order_items_file)


# --------------------------------------------------
# Order Items validation
# --------------------------------------------------

print("\n" + "=" * 70)
print("ORDER ITEMS DATA VALIDATION")
print("=" * 70)


# 1. Check missing order IDs

missing_item_order_id = order_items["order_id"].isnull().sum()

print(f"\nMissing order_id: {missing_item_order_id}")


# 2. Check missing product IDs

missing_product_id = order_items["product_id"].isnull().sum()

print(f"Missing product_id: {missing_product_id}")


# 3. Check duplicate rows

duplicate_item_rows = order_items.duplicated().sum()

print(f"Duplicate rows: {duplicate_item_rows}")


# 4. Check whether order IDs exist in Orders

invalid_order_ids = ~order_items["order_id"].isin(
    orders["order_id"]
)

invalid_order_count = invalid_order_ids.sum()

print(f"Order IDs not found in orders dataset: {invalid_order_count}")


# 5. Check whether product IDs exist in Products

# Load products dataset
products_file = DATA_DIR / "products_dataset.csv"

products = pd.read_csv(products_file)

invalid_product_ids = ~order_items["product_id"].isin(
    products["product_id"]
)

invalid_product_count = invalid_product_ids.sum()

print(f"Product IDs not found in products dataset: {invalid_product_count}")


# 6. Check negative prices

negative_prices = (order_items["price"] < 0).sum()

print(f"Negative prices: {negative_prices}")


# 7. Check negative freight values

negative_freight = (order_items["freight_value"] < 0).sum()

print(f"Negative freight values: {negative_freight}")


# --------------------------------------------------
# Final validation result
# --------------------------------------------------

if (
    missing_item_order_id == 0
    and missing_product_id == 0
    and duplicate_item_rows == 0
    and invalid_order_count == 0
    and invalid_product_count == 0
    and negative_prices == 0
    and negative_freight == 0
):
    print("\nOrder Items validation: PASSED")
else:
    print("\nOrder Items validation: REVIEW REQUIRED")

# --------------------------------------------------
# Products data validation
# --------------------------------------------------

print("\n" + "=" * 70)
print("PRODUCTS DATA VALIDATION")
print("=" * 70)


# 1. Check missing product IDs

missing_product_id = products["product_id"].isnull().sum()

print(f"\nMissing product_id: {missing_product_id}")


# 2. Check duplicate product IDs

duplicate_product_id = products["product_id"].duplicated().sum()

print(f"Duplicate product_id: {duplicate_product_id}")


# 3. Check duplicate rows

duplicate_product_rows = products.duplicated().sum()

print(f"Duplicate rows: {duplicate_product_rows}")


# 4. Check negative product weight

negative_weight = (
    products["product_weight_g"] < 0
).sum()

print(f"Negative product weight: {negative_weight}")


# 5. Check negative product dimensions

negative_length = (
    products["product_length_cm"] < 0
).sum()

negative_height = (
    products["product_height_cm"] < 0
).sum()

negative_width = (
    products["product_width_cm"] < 0
).sum()

print(f"Negative product length: {negative_length}")
print(f"Negative product height: {negative_height}")
print(f"Negative product width: {negative_width}")


# 6. Check negative number of photos

negative_photos = (
    products["product_photos_qty"] < 0
).sum()

print(f"Negative product photos: {negative_photos}")


# --------------------------------------------------
# Final validation result
# --------------------------------------------------

if (
    missing_product_id == 0
    and duplicate_product_id == 0
    and duplicate_product_rows == 0
    and negative_weight == 0
    and negative_length == 0
    and negative_height == 0
    and negative_width == 0
    and negative_photos == 0
):
    print("\nProducts validation: PASSED")
else:
    print("\nProducts validation: REVIEW REQUIRED")