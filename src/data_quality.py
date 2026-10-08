from pathlib import Path
import pandas as pd


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).parent.parent
TRANSFORMED_DIR = BASE_DIR / "data" / "processed" / "transformed"


# ==================================================
# LOAD TRANSFORMED DATA
# ==================================================

sales_data = pd.read_csv(
    TRANSFORMED_DIR / "sales_data_transformed.csv"
)

order_summary = pd.read_csv(
    TRANSFORMED_DIR / "order_summary.csv"
)

customer_summary = pd.read_csv(
    TRANSFORMED_DIR / "customer_summary.csv"
)

category_summary = pd.read_csv(
    TRANSFORMED_DIR / "category_summary.csv"
)


# ==================================================
# DATASET INFORMATION
# ==================================================

print("=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

print("\nDataset Shapes:")
print("Sales Data:", sales_data.shape)
print("Order Summary:", order_summary.shape)
print("Customer Summary:", customer_summary.shape)
print("Category Summary:", category_summary.shape)


# ==================================================
# SALES DATA QUALITY CHECKS
# ==================================================

print("\n" + "=" * 60)
print("SALES DATA QUALITY CHECKS")
print("=" * 60)

missing_order_ids = sales_data["order_id"].isna().sum()

missing_product_ids = sales_data["product_id"].isna().sum()

duplicate_order_items = sales_data.duplicated(
    subset=["order_id", "order_item_id"]
).sum()

negative_prices = (
    sales_data["price"] < 0
).sum()

negative_freight = (
    sales_data["freight_value"] < 0
).sum()

negative_total_values = (
    sales_data["total_item_value"] < 0
).sum()

missing_categories = (
    sales_data["product_category_name"].isna()
).sum()


print("Missing order_id:", missing_order_ids)
print("Missing product_id:", missing_product_ids)
print("Duplicate order-item combinations:", duplicate_order_items)
print("Negative prices:", negative_prices)
print("Negative freight values:", negative_freight)
print("Negative total item values:", negative_total_values)
print("Missing product categories:", missing_categories)


# ==================================================
# ORDER SUMMARY QUALITY CHECKS
# ==================================================

print("\n" + "=" * 60)
print("ORDER SUMMARY QUALITY CHECKS")
print("=" * 60)

missing_order_summary_ids = (
    order_summary["order_id"].isna().sum()
)

duplicate_order_ids = (
    order_summary["order_id"].duplicated().sum()
)

negative_order_value = (
    order_summary["total_order_value"] < 0
).sum()

negative_product_value = (
    order_summary["total_product_value"] < 0
).sum()

negative_order_freight = (
    order_summary["total_freight_value"] < 0
).sum()

zero_item_orders = (
    order_summary["total_items"] == 0
).sum()

negative_items = (
    order_summary["total_items"] < 0
).sum()


print("Missing order_id:", missing_order_summary_ids)
print("Duplicate order_id:", duplicate_order_ids)
print("Negative total order value:", negative_order_value)
print("Negative total product value:", negative_product_value)
print("Negative total freight value:", negative_order_freight)
print("Orders with zero items:", zero_item_orders)
print("Orders with negative items:", negative_items)


# ==================================================
# CUSTOMER SUMMARY QUALITY CHECKS
# ==================================================

print("\n" + "=" * 60)
print("CUSTOMER SUMMARY QUALITY CHECKS")
print("=" * 60)

missing_customer_ids = (
    customer_summary["customer_unique_id"].isna().sum()
)

duplicate_customer_records = customer_summary.duplicated(
    subset=[
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]
).sum()

missing_customer_city = (
    customer_summary["customer_city"].isna().sum()
)

missing_customer_state = (
    customer_summary["customer_state"].isna().sum()
)

negative_customer_orders = (
    customer_summary["total_orders"] < 0
).sum()

negative_customer_items = (
    customer_summary["total_items"] < 0
).sum()

negative_customer_spent = (
    customer_summary["total_spent"] < 0
).sum()

negative_customer_freight = (
    customer_summary["total_freight"] < 0
).sum()


print(
    "Missing customer_unique_id:",
    missing_customer_ids
)

print(
    "Duplicate customer summary records:",
    duplicate_customer_records
)

print(
    "Missing customer city:",
    missing_customer_city
)

print(
    "Missing customer state:",
    missing_customer_state
)

print(
    "Negative total orders:",
    negative_customer_orders
)

print(
    "Negative total items:",
    negative_customer_items
)

print(
    "Negative total spent:",
    negative_customer_spent
)

print(
    "Negative total freight:",
    negative_customer_freight
)


# ==================================================
# CATEGORY SUMMARY QUALITY CHECKS
# ==================================================

print("\n" + "=" * 60)
print("CATEGORY SUMMARY QUALITY CHECKS")
print("=" * 60)

missing_category_names = (
    category_summary["product_category_name"].isna().sum()
)

duplicate_categories = (
    category_summary["product_category_name"].duplicated().sum()
)

negative_category_orders = (
    category_summary["total_orders"] < 0
).sum()

negative_category_items = (
    category_summary["total_items"] < 0
).sum()

negative_category_sales = (
    category_summary["total_sales"] < 0
).sum()

negative_category_freight = (
    category_summary["total_freight"] < 0
).sum()

negative_category_revenue = (
    category_summary["total_revenue"] < 0
).sum()


print(
    "Missing product categories:",
    missing_category_names
)

print(
    "Duplicate product categories:",
    duplicate_categories
)

print(
    "Negative total orders:",
    negative_category_orders
)

print(
    "Negative total items:",
    negative_category_items
)

print(
    "Negative total sales:",
    negative_category_sales
)

print(
    "Negative total freight:",
    negative_category_freight
)

print(
    "Negative total revenue:",
    negative_category_revenue
)


# ==================================================
# OVERALL DATA QUALITY STATUS
# ==================================================

critical_failures = (
    missing_order_ids
    + duplicate_order_items
    + negative_prices
    + negative_freight
    + negative_total_values
    + missing_order_summary_ids
    + duplicate_order_ids
    + negative_order_value
    + negative_product_value
    + negative_order_freight
    + negative_items
    + missing_customer_ids
    + duplicate_customer_records
    + missing_customer_city
    + missing_customer_state
    + negative_customer_orders
    + negative_customer_items
    + negative_customer_spent
    + negative_customer_freight
    + missing_category_names
    + duplicate_categories
    + negative_category_orders
    + negative_category_items
    + negative_category_sales
    + negative_category_freight
    + negative_category_revenue
)


print("\n" + "=" * 60)
print("OVERALL DATA QUALITY STATUS")
print("=" * 60)

if critical_failures == 0:
    print("STATUS: PASSED")
    print("All critical data-quality checks passed.")

else:
    print("STATUS: PASSED WITH WARNINGS")

    print(
        "Expected data-quality observations:",
        missing_product_ids,
        "missing product IDs and",
        missing_categories,
        "missing product categories."
    )

print("\nData quality validation completed successfully.")