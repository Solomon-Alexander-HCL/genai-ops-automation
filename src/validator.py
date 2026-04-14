import sqlite3
import pandas as pd
import logging
 
logging.basicConfig(
    filename='logs/system_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
DB_PATH = "ops.db"
 
 
def run_validation():
    try:
        print("\n🔍 Step 2: Running Data Validation Checks...\n")
        logging.info("Validation started")
 
        conn = sqlite3.connect(DB_PATH)
 
        # ---------------- MISSING VALUES ----------------
        missing_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value IS NULL
        """, conn)
 
        print(f"⚠️ Missing Records Found: {len(missing_df)}")
 
        if len(missing_df) > 0:
            print("👉 Why this happens?")
            print("- Data not received from upstream system")
            print("- Delay in data feed")
            print("- System failure during ingestion\n")
 
        # ---------------- DUPLICATES ----------------
        duplicate_df = pd.read_sql("""
            SELECT event_id, COUNT(*) as count
            FROM corporate_actions
            GROUP BY event_id
            HAVING COUNT(*) > 1
        """, conn)
 
        print(f"⚠️ Duplicate Records Found: {len(duplicate_df)}")
 
        if len(duplicate_df) > 0:
            print("👉 Why duplicates occur?")
            print("- Same file processed twice")
            print("- System retry failure")
            print("- Upstream system sending duplicate records\n")
 
        # ---------------- MISMATCH ----------------
        mismatch_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value != expected_value
        """, conn)
 
        print(f"⚠️ Mismatch Records Found: {len(mismatch_df)}")
 
        if len(mismatch_df) > 0:
            print("👉 What is mismatch?")
            print("- Difference between actual value and expected value")
            print("- Example: Expected dividend = 10, Actual = 5\n")
 
            print("👉 Why mismatch happens?")
            print("- Wrong data from vendor/source system")
            print("- Delay in updates")
            print("- Manual entry mistake")
            print("- Different systems not synchronized\n")
 
        # ---------------- INVALID VALUES ----------------
        invalid_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value <= 0
        """, conn)
 
        print(f"⚠️ Invalid Records Found: {len(invalid_df)}")
 
        if len(invalid_df) > 0:
            print("👉 Why invalid values occur?")
            print("- Placeholder values (0 used temporarily)")
            print("- Data not updated properly")
            print("- Business rule violation")
            print("- Not necessarily bank mistake, but system/data pipeline issue\n")
 
        conn.close()
 
        return {
            "missing": missing_df,
            "duplicate": duplicate_df,
            "mismatch": mismatch_df,
            "invalid": invalid_df
        }
 
    except Exception as e:
        print("❌ Validation Error:", e)
        logging.error(f"Validation error: {e}")
        return None
 
 
if __name__ == "__main__":
    run_validation()