import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Define the data directory
# --------------------------------------------------

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"


# --------------------------------------------------
# 2. Define the dataset files
# --------------------------------------------------

files = {
    "Customers": "customers_dataset.csv",
    "Orders": "orders_dataset.csv",
    "Products": "products_dataset.csv"
}


# --------------------------------------------------
# 3. Function to profile a dataset
# --------------------------------------------------

def profile_dataset(name, filename):

    file_path = DATA_DIR / filename

    print("\n" + "=" * 70)
    print(f"{name.upper()} DATASET")
    print("=" * 70)

    # Check whether the file exists
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    # Read CSV
    df = pd.read_csv(file_path)

    # Basic information
    print(f"\nNumber of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")

    # Column names
    print("\nColumns:")
    for column in df.columns:
        print(f" - {column}")

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Duplicate rows
    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    # First 5 rows
    print("\nFirst 5 rows:")
    print(df.head())


# --------------------------------------------------
# 4. Profile all datasets
# --------------------------------------------------

for name, filename in files.items():
    profile_dataset(name, filename)