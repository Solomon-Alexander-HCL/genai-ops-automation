import pandas as pd
import sqlite3
import os
import logging
 
# Logging setup
logging.basicConfig(
    filename='logs/system_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
DB_PATH = "ops.db"
EXCEL_PATH = "data/corporate_actions.xlsx"
 
 
def load_excel_to_sqlite():
    try:
        print("🔄 Loading Excel file...")
        logging.info("Started loading Excel file")
 
        print("File exists:", os.path.exists(EXCEL_PATH))
 
        df = pd.read_excel(EXCEL_PATH, engine="openpyxl")
 
        print("✅ Excel Data Loaded:")
        print(df.head())
 
        logging.info(f"Loaded {len(df)} records from Excel")
 
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("corporate_actions", conn, if_exists="replace", index=False)
 
        print("✅ Data successfully loaded into SQLite database!")
        logging.info("Data loaded into SQLite successfully")
 
        conn.close()
 
    except Exception as e:
        print("❌ Error:", e)
        logging.error(f"Error in data loading: {e}")
 
 
if __name__ == "__main__":
    load_excel_to_sqlite()