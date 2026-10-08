# E-Commerce Data Engineering Pipeline

An end-to-end Data Engineering project built with **Python, SQL, and Snowflake**.

The project processes e-commerce datasets through profiling, validation, cleaning, transformation, data quality checks, and Snowflake warehousing. The final warehouse uses **RAW, STAGING, and ANALYTICS** layers.

## Architecture

```text
CSV Source Data
      ↓
Python Profiling
      ↓
Validation
      ↓
Cleaning
      ↓
Transformation
      ↓
Data Quality
      ↓
Snowflake
 ┌────┴────┐
RAW    STAGING
         ↓
      ANALYTICS
```

## Technologies

- Python
- Pandas
- NumPy
- SQL
- Snowflake
- Snowflake Connector for Python
- `write_pandas()`
- python-dotenv
- Git
- GitHub
- VS Code

## Project Structure

```text
sales-data-engineering-pipeline/
│
├── data/
│   ├── errors/
│   ├── processed/
│   │   └── transformed/
│   └── raw/
│
├── logs/
├── reports/
│
├── sql/
│   ├── database_setup.sql
│   ├── staging.sql
│   ├── analytics.sql
│   └── data_quality.sql
│
├── src/
│   ├── cleaning.py
│   ├── data_profile.py
│   ├── data_quality.py
│   ├── data_transformation.py
│   ├── data_validation.py
│   ├── main.py
│   ├── snowflake_connection.py
│   └── snowflake_load.py
│
├── tests/
├── .gitignore
└── README.md
```

## Datasets

The pipeline works with four datasets:

- Customers
- Orders
- Order Items
- Products

### Source dataset sizes

| Dataset | Rows |
|---|---:|
| Customers | 99,441 |
| Orders | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |

## Pipeline

### 1. Data Profiling

`src/data_profile.py` examines:

- Row and column counts
- Column names
- Data types
- Missing values
- Duplicate records

### 2. Data Validation

`src/data_validation.py` checks:

- Missing IDs
- Duplicate records
- Referential integrity
- Order statuses
- Date validity
- Negative prices and freight

### 3. Data Cleaning

`src/cleaning.py` standardizes:

- IDs
- City and state values
- Order status
- Numeric columns
- Date columns
- Product categories

### 4. Data Transformation

`src/data_transformation.py` joins Customers, Orders, Order Items, and Products and creates:

- Detailed sales data
- Order summaries
- Customer summaries
- Category summaries
- Purchase date attributes
- Total item value

### 5. Data Quality

`src/data_quality.py` validates:

- Missing IDs
- Duplicate records
- Negative values
- Missing product information
- Referential relationships
- Analytical summary tables

# Snowflake Data Warehouse

Database:

```text
ECOMMERCE_DB
```

Architecture:

```text
ECOMMERCE_DB
│
├── RAW
│   ├── CUSTOMERS
│   ├── ORDERS
│   ├── ORDER_ITEMS
│   └── PRODUCTS
│
├── STAGING
│   ├── CUSTOMERS
│   ├── ORDERS
│   ├── ORDER_ITEMS
│   └── PRODUCTS
│
└── ANALYTICS
    ├── SALES_DATA
    ├── ORDER_SUMMARY
    ├── CUSTOMER_SUMMARY
    └── CATEGORY_SUMMARY
```

## Snowflake Results

### RAW Layer

| Table | Rows |
|---|---:|
| CUSTOMERS | 99,441 |
| ORDERS | 99,441 |
| ORDER_ITEMS | 112,650 |
| PRODUCTS | 32,951 |

### ANALYTICS Layer

| Table | Rows |
|---|---:|
| SALES_DATA | 113,425 |
| ORDER_SUMMARY | 99,441 |
| CUSTOMER_SUMMARY | 96,219 |
| CATEGORY_SUMMARY | 73 |

## Business Results

| Metric | Value |
|---|---:|
| Total Orders | 99,441 |
| Orders With Items | 98,666 |
| Total Items | 112,650 |
| Product Sales | 13,591,643.70 |
| Freight Value | 2,251,909.54 |
| Total Revenue | 15,843,553.24 |
| Customer Summary Records | 96,219 |
| Product Categories | 73 |

## Top Product Categories by Revenue

| Rank | Category | Revenue |
|---:|---|---:|
| 1 | beleza_saude | 1,441,248.07 |
| 2 | relogios_presentes | 1,305,541.61 |
| 3 | cama_mesa_banho | 1,241,681.72 |
| 4 | esporte_lazer | 1,156,656.48 |

## Python → Snowflake

The project uses `snowflake-connector-python` and `write_pandas()` to load data into Snowflake.

Snowflake credentials are stored in environment variables.

Example:

```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ECOMMERCE_DB
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

**Never commit the real `.env` file to GitHub.**

## How to Run

### 1. Install dependencies

```bash
pip install pandas numpy snowflake-connector-python python-dotenv
```

### 2. Configure `.env`

Create the `.env` file in the project root using your own Snowflake credentials.

### 3. Test Snowflake connection

```bash
python src/snowflake_connection.py
```

Expected:

```text
Connected to Snowflake successfully!
Database: ECOMMERCE_DB
Schema: RAW
Warehouse: COMPUTE_WH
Connection closed.
```

### 4. Load source data

```bash
python src/snowflake_load.py
```

### 5. Run the Python pipeline

Recommended order:

```text
data_profile.py
      ↓
data_validation.py
      ↓
cleaning.py
      ↓
data_transformation.py
      ↓
data_quality.py
```

### 6. Run Snowflake SQL

Execute:

```text
sql/database_setup.sql
sql/staging.sql
sql/analytics.sql
sql/data_quality.sql
```

## Data Quality and Reconciliation

The project performs reconciliation between the Python pipeline and Snowflake analytical results.

Important checks include:

- Row counts
- Revenue totals
- Product sales
- Freight totals
- Item counts
- Customer counts
- Category counts

The final Snowflake results were successfully reconciled with the transformed pipeline results.

## Security

Do not commit:

```text
.env
__pycache__/
*.pyc
```

The `.gitignore` file should protect credentials and Python cache files.

## Skills Demonstrated

- Python ETL
- Pandas
- SQL
- Snowflake
- Data Warehousing
- ETL / ELT
- Data Cleaning
- Data Validation
- Data Transformation
- Data Quality
- Data Modeling
- Joins
- Aggregations
- Referential Integrity
- Environment Variables
- Git and GitHub

## Future Improvements

- Apache Airflow orchestration
- Incremental data loading
- Snowflake Streams and Tasks
- Automated unit tests
- Pipeline monitoring
- BI dashboard
- GitHub Actions CI/CD
- Additional business KPIs

## Author

**MD Azam**

B.Sc. Computer Science  
Aspiring Data Engineer

**Skills:** Python | SQL | Snowflake | Pandas | Data Engineering

## License

This project is intended for educational, portfolio, and demonstration purposes.
