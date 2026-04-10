import pandas as pd
import sqlite3
import os
 
# Database file
DB_PATH = "ops.db"
 
# Excel file path
EXCEL_PATH = "data/corporate_actions.xlsx"
 
 
def load_excel_to_sqlite():
    try:
        print("🔄 Loading Excel file...")
 
        # Read Excel
        df = pd.read_excel(EXCEL_PATH, engine="openpyxl")
 
        print("✅ Excel Data Loaded:")
        print(df.head())
 
        # Connect to SQLite
        conn = sqlite3.connect(DB_PATH)
 
        # Store in DB
        df.to_sql("corporate_actions", conn, if_exists="replace", index=False)
 
        print("✅ Data successfully loaded into SQLite database!")
 
        conn.close()
 
    except Exception as e:
        print("❌ Error:", e)
 
 
if __name__ == "__main__":
    load_excel_to_sqlite()