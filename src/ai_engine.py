def generate_ai_analysis(issue_type, row):
    """
    Simulated AI logic for root cause, risk and resolution
    """
 
    event_id = row.get("event_id", "N/A")
    stock = row.get("stock", "Unknown")
 
    if issue_type == "MISSING":
        return {
            "root_cause": "Upstream data source failed to provide value",
            "risk": "HIGH",
            "suggestion": "Check source system and reprocess missing data"
        }
 
    elif issue_type == "DUPLICATE":
        return {
            "root_cause": "Duplicate data ingestion from upstream system",
            "risk": "MEDIUM",
            "suggestion": "Remove duplicate records and validate ingestion logic"
        }
 
    elif issue_type == "MISMATCH":
        return {
            "root_cause": f"Mismatch between expected and actual values for {stock}",
            "risk": "HIGH",
            "suggestion": "Validate corporate action feed and correct value before posting"
        }
 
    elif issue_type == "INVALID":
        return {
            "root_cause": "Invalid value detected (zero or negative)",
            "risk": "HIGH",
            "suggestion": "Check business rules and correct invalid data"
        }
 
    else:
        return {
            "root_cause": "Unknown issue",
            "risk": "LOW",
            "suggestion": "Manual investigation required"
        }
 