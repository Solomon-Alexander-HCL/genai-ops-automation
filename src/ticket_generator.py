import pandas as pd
from datetime import datetime
from ai_engine import generate_ai_analysis

OUTPUT_PATH = "output/tickets.csv"
 
 
def generate_ticket(issue_type, row):
    """
    Create a structured ticket for each issue
    """
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
 
    # Add logic for each issue type
    if issue_type == "MISSING":
        ticket["description"] = "Missing value detected in corporate action data"
        ticket["priority"] = "HIGH"
 
    elif issue_type == "DUPLICATE":
        ticket["description"] = "Duplicate event detected"
        ticket["priority"] = "MEDIUM"
 
    elif issue_type == "MISMATCH":
        ticket["description"] = "Value mismatch between actual and expected"
        ticket["priority"] = "HIGH"
 
    elif issue_type == "INVALID":
        ticket["description"] = "Invalid value (zero or negative)"
        ticket["priority"] = "HIGH"
 
    return ticket
 
 
def create_tickets(validation_results):
    all_tickets = []
 
    # Missing
    for _, row in validation_results["missing"].iterrows():
        all_tickets.append(generate_ticket("MISSING", row))
 
    # Duplicate (special handling)
    for _, row in validation_results["duplicate"].iterrows():
        all_tickets.append({
            "ticket_id": f"TICK-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "issue_type": "DUPLICATE",
            "event_id": row["event_id"],
            "stock": "N/A",
            "description": f"Duplicate event_id found ({row['count']} times)",
            "priority": "MEDIUM",
            "status": "OPEN",
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
 
    # Mismatch
    for _, row in validation_results["mismatch"].iterrows():
        all_tickets.append(generate_ticket("MISMATCH", row))
 
    # Invalid
    for _, row in validation_results["invalid"].iterrows():
        all_tickets.append(generate_ticket("INVALID", row))
 
    # Convert to DataFrame
    tickets_df = pd.DataFrame(all_tickets)
 
    # Save to CSV
    tickets_df.to_csv(OUTPUT_PATH, index=False)
 
    print(f"\n🎫 {len(tickets_df)} Tickets Generated Successfully!")
    print(f"📁 Saved to: {OUTPUT_PATH}")
 
    return tickets_df
 