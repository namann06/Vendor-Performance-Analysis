import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Define directory paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "ingestion_db.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# Connect to SQLite database in the project root
db_path = os.path.join(PROJECT_ROOT, 'inventory.db')
engine = create_engine(f'sqlite:///{db_path}')

def ingest_db(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

def load_raw_data():
    raw_dir = os.path.join(PROJECT_ROOT, 'data', 'raw')
    
    csv_files = [
        'begin_inventory.csv',
        'end_inventory.csv',
        'purchase_prices.csv',
        'purchases.csv',
        'sales.csv',
        'vendor_invoice.csv'
    ]

    start = time.time()
    
    for file in csv_files:
        # Check root folder first (for full datasets)
        root_path = os.path.join(PROJECT_ROOT, file)
        raw_path = os.path.join(raw_dir, file)
        
        if os.path.exists(root_path):
            file_path = root_path
            print(f"Ingesting full dataset '{file}' from project root...")
            logging.info(f"Ingesting full dataset '{file}' from root: {root_path}")
        elif os.path.exists(raw_path):
            file_path = raw_path
            print(f"Ingesting sample dataset '{file}' from data/raw/...")
            logging.info(f"Ingesting sample dataset '{file}' from raw: {raw_path}")
        else:
            print(f"Warning: Dataset file '{file}' not found in root or data/raw/")
            logging.warning(f"Dataset file '{file}' not found in root or raw")
            continue
            
        df = pd.read_csv(file_path, low_memory=False)
        ingest_db(df, file[:-4], engine)
        
    end = time.time()
    total_time = (end - start) / 60
    logging.info('--------------Ingestion Complete----------')
    logging.info(f'Total Time Taken : {total_time:.4f} minutes')
    print(f"-------------- Ingestion Complete --------------")
    print(f"Total Time Taken: {total_time * 60:.2f} seconds ({total_time:.4f} minutes)")

if __name__ == '__main__':
    load_raw_data()
