import pandas as pd
import sqlite3
import os
import logging
 
# Logging setup (acts like Splunk monitoring)
logging.basicConfig(
    filename='logs/system_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
DB_PATH = "ops.db"
EXCEL_PATH = "data/corporate_actions.xlsx"
 
 
def load_excel_to_sqlite():
    try:
        print("\n🔄 Step 1: Loading Corporate Action Data...\n")
        logging.info("Started loading Excel file")
 
        # Check if file exists
        print("📁 Checking if input file exists...")
        print("File exists:", os.path.exists(EXCEL_PATH))
 
        # Read Excel
        df = pd.read_excel(EXCEL_PATH, engine="openpyxl")
 
        print("\n📊 Sample Data Loaded:")
        print(df.head())
 
        # Explanation
        print("\n🧠 Explanation:")
        print("This data represents corporate actions like dividends, splits, etc.")
        print("In real systems, this data comes from upstream financial systems.\n")
 
        logging.info(f"Loaded {len(df)} records")
 
        # Store into SQLite DB
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("corporate_actions", conn, if_exists="replace", index=False)
 
        print("✅ Data successfully stored into database (SQLite)")
        print("👉 This simulates data ingestion into production database\n")
 
        conn.close()
 
    except Exception as e:
        print("❌ Error:", e)
        logging.error(f"Error in data loading: {e}")
 
 
if __name__ == "__main__":
    load_excel_to_sqlite()