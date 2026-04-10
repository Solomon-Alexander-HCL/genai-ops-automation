from data_loader import load_excel_to_sqlite
from validator import run_validation
from ticket_generator import create_tickets
 
 
def main():
    print("🚀 Starting GenAI Ops Automation...\n")
 
    # Step 1: Load Data
    load_excel_to_sqlite()
 
    # Step 2: Validate Data
    results = run_validation()
 
    # Step 3: Generate Tickets
    if results:
        create_tickets(results)
 
 
if __name__ == "__main__":
    main()