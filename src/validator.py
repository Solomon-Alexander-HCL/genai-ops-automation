import sqlite3
import pandas as pd
 
DB_PATH = "ops.db"
 
 
def run_validation():
    try:
        print("\n🔍 Running Data Validation Checks...\n")
 
        conn = sqlite3.connect(DB_PATH)
 
        # 1. Missing Values
        missing_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value IS NULL
        """, conn)
 
        print(f"⚠️ Missing Records: {len(missing_df)}")
 
        # 2. Duplicate Records
        duplicate_df = pd.read_sql("""
            SELECT event_id, COUNT(*) as count
            FROM corporate_actions
            GROUP BY event_id
            HAVING COUNT(*) > 1
        """, conn)
 
        print(f"⚠️ Duplicate Records: {len(duplicate_df)}")
 
        # 3. Value Mismatch
        mismatch_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value != expected_value
        """, conn)
 
        print(f"⚠️ Mismatch Records: {len(mismatch_df)}")
 
        # 4. Invalid Values (0 or negative)
        invalid_df = pd.read_sql("""
            SELECT * FROM corporate_actions
            WHERE value <= 0
        """, conn)
 
        print(f"⚠️ Invalid Records: {len(invalid_df)}")
 
        conn.close()
 
        return {
            "missing": missing_df,
            "duplicate": duplicate_df,
            "mismatch": mismatch_df,
            "invalid": invalid_df
        }
 
    except Exception as e:
        print("❌ Validation Error:", e)
        return None
 
 
if __name__ == "__main__":
    results = run_validation()
 
    # Debug print
    if results:
        for key, df in results.items():
            print(f"\n📌 {key.upper()} DATA:")
            print(df)