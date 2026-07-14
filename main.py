# ==============================================================================
# MODULE: main.py
# DESCRIPTION: Orchestrates execution pipeline and syncing parameters.
# ==============================================================================

import json
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from extraction.scraper import run_scraper

def push_to_google_sheet(leads, spreadsheet_id):
    """Pushes verified, mathematically unrepeated streams into storage tracking matrices."""
    print("📡 Connecting to Google Sheets API Core...")
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id).worksheet("Prospects")
        
        history_file = "scraped_history.json"
        local_history = []
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as f: 
                local_history = json.load(f)
        local_history_set = set(local_history)

        added_count = 0
        for lead in leads:
            web = lead["website"]
            
            # Universal script lifetime verification boundary
            if web in local_history_set:
                continue 
                
            row = [
                lead["name"], lead["website"], "", lead["legal_form"], lead["employees"],
                lead["owner"], "", "", "HWK directory", "", "", "", "", "", "",
                lead["email"], lead["phone"], lead["social"]
            ]
            sheet.append_row(row)
            local_history.append(web)
            local_history_set.add(web)
            added_count += 1
            
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(local_history, f, indent=4)
            
        print(f"📊 Successfully pushed {added_count} BRAND NEW, unique rows to Google Sheet.")
    except Exception as e:
        print(f"❌ Sheets Sync Failed: {str(e)}")

def main():
    """Initializes and runs the lead parsing automation stack pipeline."""
    print("🚀 Starting Magentis Automation Pipeline Core...")
    raw_leads = run_scraper()
    
    with open("raw_leads.json", "w", encoding="utf-8") as file:
        json.dump(raw_leads, file, indent=4, ensure_ascii=False)
        
    TARGET_SPREADSHEET_ID = "1GVUpmK6PQDOD_fuYI4ZaGmtrzQ_Hvm-GIEJ4duLQaH8"
    push_to_google_sheet(raw_leads, TARGET_SPREADSHEET_ID)

if __name__ == "__main__":
    main()