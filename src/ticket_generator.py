import pandas as pd
from datetime import datetime
import logging
from ai_engine import generate_ai_analysis
 
# Logging setup (acts like Splunk monitoring)
logging.basicConfig(
    filename='logs/system_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
OUTPUT_PATH = "output/tickets.csv"
 
 
def generate_ticket(issue_type, row):
    """
    This function creates a structured ticket for each issue detected.
    It simulates how ServiceNow tickets are created in real production systems.
    """
 
    # Get AI-based analysis (root cause, risk, suggestion)
    ai_data = generate_ai_analysis(issue_type, row)
 
    ticket = {
        "ticket_id": f"TICK-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "issue_type": issue_type,
        "event_id": row.get("event_id", "N/A"),
        "stock": row.get("stock", "N/A"),
 
        # Business explanation of issue
        "description": f"{issue_type} issue detected in corporate action data",
 
        # Priority based on AI risk
        "priority": ai_data["risk"],
 
        "status": "OPEN",
 
        # AI-generated insights
        "root_cause": ai_data["root_cause"],
        "suggestion": ai_data["suggestion"],
 
        # Timestamp
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    return ticket
 
 
def create_tickets(validation_results):
    """
    This function converts validation results into tickets.
    Each issue becomes one ticket.
    """
 
    all_tickets = []
 
    print("\n🎫 Step 3: Generating Incident Tickets...\n")
    logging.info("Ticket generation started")
 
    # ---------------- MISSING ----------------
    for _, row in validation_results["missing"].iterrows():
        print(f"➡️ Creating ticket for MISSING value (Event ID: {row.get('event_id')})")
        all_tickets.append(generate_ticket("MISSING", row))
 
    # ---------------- DUPLICATE ----------------
    for _, row in validation_results["duplicate"].iterrows():
        print(f"➡️ Creating ticket for DUPLICATE event_id ({row['event_id']})")
 
        all_tickets.append({
            "ticket_id": f"TICK-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "issue_type": "DUPLICATE",
            "event_id": row["event_id"],
            "stock": "N/A",
 
            "description": f"Duplicate event_id found ({row['count']} times)",
            "priority": "MEDIUM",
            "status": "OPEN",
 
            "root_cause": "Same data processed multiple times or duplicate ingestion",
            "suggestion": "Remove duplicate records and check ingestion process",
 
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
 
    # ---------------- MISMATCH ----------------
    for _, row in validation_results["mismatch"].iterrows():
        print(f"➡️ Creating ticket for MISMATCH (Event ID: {row.get('event_id')})")
        all_tickets.append(generate_ticket("MISMATCH", row))
 
    # ---------------- INVALID ----------------
    for _, row in validation_results["invalid"].iterrows():
        print(f"➡️ Creating ticket for INVALID value (Event ID: {row.get('event_id')})")
        all_tickets.append(generate_ticket("INVALID", row))
 
    # Convert to DataFrame
    tickets_df = pd.DataFrame(all_tickets)
 
    # Save output
    tickets_df.to_csv(OUTPUT_PATH, index=False)
 
    # ---------------- FINAL OUTPUT EXPLANATION ----------------
    print("\n📊 Ticket Generation Completed!\n")
 
    print("🧠 Explanation of Output:")
    print("Each row in tickets.csv represents an incident detected in the system.\n")
 
    print("Fields included:")
    print("- ticket_id → Unique identifier (like ServiceNow ticket)")
    print("- issue_type → Type of problem (Missing, Duplicate, etc.)")
    print("- event_id → Affected record")
    print("- root_cause → Why issue occurred (AI analysis)")
    print("- suggestion → Recommended fix")
    print("- priority → Risk level (High/Medium/Low)\n")
 
    print(f"🎯 Total Tickets Generated: {len(tickets_df)}")
    print(f"📁 Saved to: {OUTPUT_PATH}\n")
 
    logging.info(f"{len(tickets_df)} tickets generated successfully")
 
    return tickets_df