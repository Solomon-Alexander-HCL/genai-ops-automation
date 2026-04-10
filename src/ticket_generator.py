import pandas as pd
from datetime import datetime
import logging
from ai_engine import generate_ai_analysis
 
# Logging setup
logging.basicConfig(
    filename='logs/system_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
OUTPUT_PATH = "output/tickets.csv"
 
 
def generate_ticket(issue_type, row):
    ai_data = generate_ai_analysis(issue_type, row)
 
    ticket = {
        "ticket_id": f"TICK-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "issue_type": issue_type,
        "event_id": row.get("event_id", "N/A"),
        "stock": row.get("stock", "N/A"),
        "description": "",
        "priority": ai_data["risk"],
        "status": "OPEN",
        "root_cause": ai_data["root_cause"],
        "suggestion": ai_data["suggestion"],
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    return ticket
 
 
def create_tickets(validation_results):
    all_tickets = []
 
    logging.info("Ticket generation started")
 
    # Missing
    for _, row in validation_results["missing"].iterrows():
        all_tickets.append(generate_ticket("MISSING", row))
 
    # Duplicate
    for _, row in validation_results["duplicate"].iterrows():
        all_tickets.append({
            "ticket_id": f"TICK-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "issue_type": "DUPLICATE",
            "event_id": row["event_id"],
            "stock": "N/A",
            "description": f"Duplicate event_id found ({row['count']} times)",
            "priority": "MEDIUM",
            "status": "OPEN",
            "root_cause": "Duplicate data ingestion",
            "suggestion": "Remove duplicate records",
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
 
    # Mismatch
    for _, row in validation_results["mismatch"].iterrows():
        all_tickets.append(generate_ticket("MISMATCH", row))
 
    # Invalid
    for _, row in validation_results["invalid"].iterrows():
        all_tickets.append(generate_ticket("INVALID", row))
 
    tickets_df = pd.DataFrame(all_tickets)
    tickets_df.to_csv(OUTPUT_PATH, index=False)
 
    print(f"\n🎫 {len(tickets_df)} Tickets Generated Successfully!")
    print(f"📁 Saved to: {OUTPUT_PATH}")
 
    logging.info(f"{len(tickets_df)} tickets generated and saved")
 
    return tickets_df