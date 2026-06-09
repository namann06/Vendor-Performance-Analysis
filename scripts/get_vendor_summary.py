# Import required libraries for database connection, data handling, and logging
import sqlite3
import pandas as pd
import logging
import os
import sys

# Define directory paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.append(SCRIPT_DIR)

# Import ingestion function from local script
from ingestion_db import ingest_db

# ------------------- LOGGER SETUP -------------------
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Create custom logger
logger = logging.getLogger("vendor_summary_logger")
logger.setLevel(logging.DEBUG)

# Create file handler
log_file_path = os.path.join(LOGS_DIR, "get_vendor_summary.log")
file_handler = logging.FileHandler(log_file_path)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# Attach handler to logger
logger.addHandler(file_handler)


# ------------------- SQL SUMMARY FUNCTION -------------------

# Function to create a vendor summary by merging multiple tables
# It aggregates freight, purchase, and pricing data to build a vendor-level summary dataset
def create_vendor_summary(conn):

    """
    This function merges different tables to get the overall vendor summary
    and adds new columns in the resultant data.
    """

    vendor_sales_summary = pd.read_sql_query("""

        WITH FreightSummary AS (
            SELECT
                VendorNumber,
                SUM(Freight) AS FreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        ),

        PurchaseSummary AS (
            SELECT
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price AS ActualPrice,
                pp.Volume,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            JOIN purchase_prices pp
                ON p.Brand = pp.Brand
            WHERE p.PurchasePrice > 0
            GROUP BY
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price,
                pp.Volume
        ),

        SalesSummary AS (
            SELECT
                VendorNo,
                Brand,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(SalesDollars) AS TotalSalesDollars,
                SUM(SalesPrice) AS TotalSalesPrice,
                SUM(ExciseTax) AS TotalExciseTax
            FROM sales
            GROUP BY VendorNo, Brand
        )

        SELECT
            ps.VendorNumber,
            ps.VendorName,
            ps.Brand,
            ps.Description,
            ps.PurchasePrice,
            ps.ActualPrice,
            ps.Volume,
            ps.TotalPurchaseQuantity,
            ps.TotalPurchaseDollars,
            ss.TotalSalesQuantity,
            ss.TotalSalesDollars,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.FreightCost
        FROM PurchaseSummary ps

        LEFT JOIN SalesSummary ss
            ON ps.VendorNumber = ss.VendorNo
            AND ps.Brand = ss.Brand

        LEFT JOIN FreightSummary fs
            ON ps.VendorNumber = fs.VendorNumber

        ORDER BY ps.TotalPurchaseDollars DESC

    """, conn)

    return vendor_sales_summary


# ------------------- DATA CLEANING FUNCTION -------------------

# Function to clean and prepare the vendor summary data
def clean_data(df):

    """
    This function cleans the data and creates additional analytical columns.
    """

    # changing datatype to float
    df["Volume"] = df["Volume"].astype("float")

    # filling missing values with 0
    df.fillna(0, inplace=True)

    # removing spaces from categorical columns
    df["VendorName"] = df["VendorName"].str.strip()
    df["Description"] = df["Description"].str.strip()

    # creating new columns for better analysis
    df["GrossProfit"] = df["TotalSalesDollars"] - df["TotalPurchaseDollars"]

    # Prevent division by zero
    df["ProfitMargin"] = df.apply(
        lambda row: (row["GrossProfit"] / row["TotalSalesDollars"]) * 100 if row["TotalSalesDollars"] != 0 else 0,
        axis=1
    )

    df["StockTurnover"] = df.apply(
        lambda row: (row["TotalSalesQuantity"] / row["TotalPurchaseQuantity"]) if row["TotalPurchaseQuantity"] != 0 else 0,
        axis=1
    )

    df["SalesToPurchaseRatio"] = df.apply(
        lambda row: (row["TotalSalesDollars"] / row["TotalPurchaseDollars"]) if row["TotalPurchaseDollars"] != 0 else 0,
        axis=1
    )

    return df


# ------------------- MAIN PIPELINE -------------------

# Connects to the database, creates the vendor summary,
# cleans the data, and stores the processed data back into the database
if __name__ == "__main__":

    # creating database connection
    db_path = os.path.join(PROJECT_ROOT, "inventory.db")
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)

    logger.info("Creating Vendor Summary Table.....")
    print("Generating vendor sales summary using SQL query...")
    summary_df = create_vendor_summary(conn)
    logger.info(summary_df.head())

    logger.info("Cleaning Data.....")
    print("Cleaning data and computing metrics...")
    clean_df = clean_data(summary_df)
    logger.info(clean_df.head())

    logger.info("Ingesting data to DB.....")
    print("Ingesting processed summary back into the database...")
    ingest_db(clean_df, "vendor_sales_summary", conn)

    # Save to data/processed CSV for GitHub repository inclusion
    processed_csv_path = os.path.join(PROJECT_ROOT, "data", "processed", "vendor_sales_summary.csv")
    os.makedirs(os.path.dirname(processed_csv_path), exist_ok=True)
    clean_df.to_csv(processed_csv_path, index=False)
    logger.info(f"Saved processed CSV summary to {processed_csv_path}")
    print(f"Saved processed CSV summary to {processed_csv_path}")

    logger.info("Completed")
    print("Summary generation complete!")
