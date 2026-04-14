def generate_ai_analysis(issue_type, row):
    """
    This function simulates AI reasoning.
    It explains WHY issue occurred and WHAT to do.
    """
 
    if issue_type == "MISSING":
        return {
            "root_cause": "Data not received from upstream system",
            "risk": "HIGH",
            "suggestion": "Reprocess data or check source system"
        }
 
    elif issue_type == "DUPLICATE":
        return {
            "root_cause": "Duplicate ingestion of same data",
            "risk": "MEDIUM",
            "suggestion": "Remove duplicate records and fix ingestion logic"
        }
 
    elif issue_type == "MISMATCH":
        return {
            "root_cause": "Actual value does not match expected/reference value",
            "risk": "HIGH",
            "suggestion": "Validate data with trusted source"
        }
 
    elif issue_type == "INVALID":
        return {
            "root_cause": "Invalid or placeholder value detected",
            "risk": "HIGH",
            "suggestion": "Correct data based on business rules"
        }
 
    else:
        return {
            "root_cause": "Unknown issue",
            "risk": "LOW",
            "suggestion": "Manual investigation required"
        }
 