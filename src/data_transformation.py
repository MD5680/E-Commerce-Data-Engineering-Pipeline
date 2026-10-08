import pandas as pd
from pathlib import Path


# =========================
# PROJECT DIRECTORIES
# =========================

BASE_DIR = Path(__file__).parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR = BASE_DIR / "data" / "processed" / "transformed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# LOAD CLEANED DATASETS
# =========================

customers = pd.read_csv(
    PROCESSED_DIR / "customers_cleaned.csv"
)

orders = pd.read_csv(
    PROCESSED_DIR / "orders_cleaned.csv"
)

order_items = pd.read_csv(
    PROCESSED_DIR / "order_items_cleaned.csv"
)

products = pd.read_csv(
    PROCESSED_DIR / "products_cleaned.csv"
)


# =========================
# DISPLAY DATASET SIZES
# =========================

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Products:", products.shape)

print("\nAll cleaned datasets loaded successfully.")


# =========================
# JOIN ORDERS + CUSTOMERS
# =========================

orders_customers = orders.merge(
    customers,
    on="customer_id",
    how="left"
)


# =========================
# CHECK RESULT
# =========================

print("\nOrders + Customers:")
print(orders_customers.shape)

print("\nColumns:")
print(orders_customers.columns.tolist())

print("\nSample data:")
print(orders_customers.head())

# =========================
# JOIN WITH ORDER ITEMS
# =========================

orders_customers_items = orders_customers.merge(
    order_items,
    on="order_id",
    how="left"
)


# =========================
# CHECK RESULT
# =========================

print("\nOrders + Customers + Order Items:")
print(orders_customers_items.shape)

print("\nColumns:")
print(orders_customers_items.columns.tolist())

print("\nSample data:")
print(orders_customers_items.head())


# =========================
# JOIN WITH PRODUCTS
# =========================

sales_data = orders_customers_items.merge(
    products,
    on="product_id",
    how="left"
)


# =========================
# CHECK FINAL RESULT
# =========================

print("\nFinal Sales Dataset:")
print(sales_data.shape)

print("\nColumns:")
print(sales_data.columns.tolist())

print("\nSample data:")
print(sales_data.head())


# =========================
# CREATE BUSINESS COLUMNS
# =========================

# Make sure purchase timestamp is datetime
sales_data["order_purchase_timestamp"] = pd.to_datetime(
    sales_data["order_purchase_timestamp"],
    errors="coerce"
)


# Total value for each order item
sales_data["total_item_value"] = (
    sales_data["price"] + sales_data["freight_value"]
)

# =========================
# ORDER-LEVEL AGGREGATION
# =========================

order_summary = (
    sales_data
    .groupby("order_id", as_index=False)
    .agg(
        total_order_value=("total_item_value", "sum"),
        total_product_value=("price", "sum"),
        total_freight_value=("freight_value", "sum"),
        total_items=("order_item_id", "count")
    )
)


# =========================
# CHECK ORDER SUMMARY
# =========================

print("\nOrder Summary:")
print(order_summary.shape)

print("\nOrder Summary Sample:")
print(order_summary.head())


# Extract purchase date
sales_data["purchase_date"] = (
    sales_data["order_purchase_timestamp"].dt.date
)


# Extract purchase year
sales_data["purchase_year"] = (
    sales_data["order_purchase_timestamp"].dt.year
)


# Extract purchase month
sales_data["purchase_month"] = (
    sales_data["order_purchase_timestamp"].dt.month
)


# Extract purchase year-month
sales_data["purchase_year_month"] = (
    sales_data["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

# =========================
# CUSTOMER-LEVEL AGGREGATION
# =========================

customer_summary = (
    sales_data
    .groupby(
        [
            "customer_unique_id",
            "customer_city",
            "customer_state"
        ],
        as_index=False
    )
    .agg(
        total_orders=("order_id", "nunique"),
        total_items=("order_item_id", "count"),
        total_spent=("total_item_value", "sum"),
        total_freight=("freight_value", "sum")
    )
)


# =========================
# CHECK CUSTOMER SUMMARY
# =========================

print("\nCustomer Summary:")
print(customer_summary.shape)

print("\nCustomer Summary Sample:")
print(customer_summary.head())

# =========================
# PRODUCT CATEGORY SUMMARY
# =========================

category_summary = (
    sales_data
    .groupby(
        "product_category_name",
        as_index=False
    )
    .agg(
        total_orders=("order_id", "nunique"),
        total_items=("order_item_id", "count"),
        total_sales=("price", "sum"),
        total_freight=("freight_value", "sum"),
        total_revenue=("total_item_value", "sum")
    )
)


# =========================
# SORT BY REVENUE
# =========================

category_summary = category_summary.sort_values(
    by="total_revenue",
    ascending=False
)


# =========================
# CHECK CATEGORY SUMMARY
# =========================

print("\nProduct Category Summary:")
print(category_summary.shape)

print("\nTop 10 Categories:")
print(category_summary.head(10))


# =========================
# CHECK NEW COLUMNS
# =========================

print("\nBusiness columns created:")

print(
    sales_data[
        [
            "order_id",
            "price",
            "freight_value",
            "total_item_value",
            "purchase_date",
            "purchase_year",
            "purchase_month",
            "purchase_year_month"
        ]
    ].head()
)


# Extract purchase year
sales_data["purchase_year"] = (
    sales_data["order_purchase_timestamp"]
    .dt.year
)


# Extract purchase month
sales_data["purchase_month"] = (
    sales_data["order_purchase_timestamp"]
    .dt.month
)


# Extract purchase year-month
sales_data["purchase_year_month"] = (
    sales_data["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)


# =========================
# CHECK NEW COLUMNS
# =========================

print("\nBusiness columns created:")

print(
    sales_data[
        [
            "order_id",
            "price",
            "freight_value",
            "total_item_value",
            "purchase_date",
            "purchase_year",
            "purchase_month",
            "purchase_year_month"
        ]
    ].head()
)

# =========================
# CONVERT DATE COLUMNS
# =========================

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
        errors="coerce"
    )

# Convert order item shipping date
order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

# =========================
# SAVE TRANSFORMED DATA
# =========================

sales_data.to_csv(
    OUTPUT_DIR / "sales_data_transformed.csv",
    index=False
)

order_summary.to_csv(
    OUTPUT_DIR / "order_summary.csv",
    index=False
)

customer_summary.to_csv(
    OUTPUT_DIR / "customer_summary.csv",
    index=False
)

category_summary.to_csv(
    OUTPUT_DIR / "category_summary.csv",
    index=False
)


# =========================
# FINAL OUTPUT MESSAGE
# =========================

print("\nTransformed datasets saved successfully.")

print(
    "Sales data:",
    OUTPUT_DIR / "sales_data_transformed.csv"
)

print(
    "Order summary:",
    OUTPUT_DIR / "order_summary.csv"
)

print(
    "Customer summary:",
    OUTPUT_DIR / "customer_summary.csv"
)

print(
    "Category summary:",
    OUTPUT_DIR / "category_summary.csv"
)