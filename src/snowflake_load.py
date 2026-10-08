import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# 1. Snowflake connection
# -----------------------------
connection = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

print("Connected to Snowflake!")

# -----------------------------
# 2. Load Products CSV
# -----------------------------
file_path = "data/raw/products_dataset.csv"

products = pd.read_csv(file_path)

print("Products CSV loaded.")
print("Rows:", len(products))
print("Columns:", len(products.columns))

# -----------------------------
# 3. Uppercase column names
# -----------------------------
products.columns = products.columns.str.upper()

# Handle possible Olist spelling
# differences in the original dataset
products = products.rename(columns={
    "PRODUCT_NAME_LENGHT": "PRODUCT_NAME_LENGTH",
    "PRODUCT_DESCRIPTION_LENGHT": "PRODUCT_DESCRIPTION_LENGTH"
})

print("\nColumns:")
print(products.columns.tolist())

# -----------------------------
# 4. Convert numeric columns
# -----------------------------
numeric_columns = [
    "PRODUCT_NAME_LENGTH",
    "PRODUCT_DESCRIPTION_LENGTH",
    "PRODUCT_PHOTOS_QTY",
    "PRODUCT_WEIGHT_G",
    "PRODUCT_LENGTH_CM",
    "PRODUCT_HEIGHT_CM",
    "PRODUCT_WIDTH_CM"
]

for column in numeric_columns:
    products[column] = pd.to_numeric(
        products[column],
        errors="coerce"
    )

print("\nNumeric columns converted successfully.")

# -----------------------------
# 5. Load into Snowflake
# -----------------------------
success, nchunks, nrows, _ = write_pandas(
    conn=connection,
    df=products,
    table_name="PRODUCTS",
    schema="RAW",
    database="ECOMMERCE_DB",
    auto_create_table=False,
    overwrite=True
)

print("\nSnowflake load completed!")
print("Success:", success)
print("Chunks:", nchunks)
print("Rows loaded:", nrows)

# -----------------------------
# 6. Verify row count
# -----------------------------
cursor = connection.cursor()

cursor.execute("""
    SELECT COUNT(*)
    FROM ECOMMERCE_DB.RAW.PRODUCTS
""")

row_count = cursor.fetchone()[0]

print("Rows in Snowflake:", row_count)

cursor.close()
connection.close()

print("\nSnowflake connection closed.")