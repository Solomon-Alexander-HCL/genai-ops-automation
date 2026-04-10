import sqlite3
import pandas as pd
import logging
 
# Logging setup
logging.basicConfig(
    filename='logs/system_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
DB_PATH = "ops.db"
 
 
def run_validation():
    try:
        print("\n🔍 Running Data Validation Checks...\n")
        logging.info("Validation started")
 
        conn = sqlite3.connect(DB_PATH)
 
        # Missing Values
        missing_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value IS NULL
        """, conn)
 
        print(f"⚠️ Missing Records: {len(missing_df)}")
        logging.info(f"Missing Records: {len(missing_df)}")
 
        # Duplicate Records
        duplicate_df = pd.read_sql("""
            SELECT event_id, COUNT(*) as count
            FROM corporate_actions
            GROUP BY event_id
            HAVING COUNT(*) > 1
        """, conn)
 
        print(f"⚠️ Duplicate Records: {len(duplicate_df)}")
        logging.info(f"Duplicate Records: {len(duplicate_df)}")
 
        # Mismatch
        mismatch_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value != expected_value
        """, conn)
 
        print(f"⚠️ Mismatch Records: {len(mismatch_df)}")
        logging.info(f"Mismatch Records: {len(mismatch_df)}")
 
        # Invalid
        invalid_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value <= 0
        """, conn)
 
        print(f"⚠️ Invalid Records: {len(invalid_df)}")
        logging.info(f"Invalid Records: {len(invalid_df)}")
 
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