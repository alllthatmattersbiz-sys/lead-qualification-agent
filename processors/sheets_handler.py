from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

def get_sheets_service():
    """Initialize Google Sheets API service."""
    try:
        creds = Credentials.from_service_account_file(
            'google_credentials.json',
            scopes=SCOPES
        )
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Error initializing Sheets service: {e}")
        return None


def create_spreadsheet(title="AI Lead Qualified Leads"):
    """Create a new Google Sheet if it doesn't exist."""
    try:
        service = build('sheets', 'v4', credentials=Credentials.from_service_account_file(
            'google_credentials.json',
            scopes=SCOPES
        ))
        
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        
        result = service.spreadsheets().create(body=spreadsheet).execute()
        sheet_id = result['spreadsheetId']
        print(f"✅ Created new spreadsheet: {sheet_id}")
        return sheet_id
    
    except Exception as e:
        print(f"Error creating spreadsheet: {e}")
        return None


def save_leads_to_sheets(qualified_leads: list) -> bool:
    """Save qualified leads to Google Sheet."""
    
    if not SHEET_ID:
        print("❌ GOOGLE_SHEET_ID not set in .env")
        return False
    
    try:
        service = get_sheets_service()
        if not service:
            return False
        
        # Prepare data
        headers = ['Date', 'Score', 'Status', 'Author', 'Company', 'Source', 'Opportunity', 'Budget', 'Timeline', 'Email Subject', 'Email Opening', 'Link']
        
        rows = [headers]
        
        for lead in qualified_leads:
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                lead.get('score', '?'),
                'Qualified' if lead.get('is_qualified') else 'Not Qualified',
                lead['author'],
                lead.get('company_name', 'Unknown'),
                lead['source'],
                lead.get('opportunity', '')[:50],
                lead.get('budget_signal', 'N/A')[:30],
                lead.get('timeline', 'N/A')[:20],
                lead.get('email_subject', '')[:50],
                lead.get('email_opening', '')[:100],
                lead.get('hn_link', '')
            ]
            rows.append(row)
        
        # Write to sheet
        body = {
            'values': rows
        }
        
        result = service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range='Sheet1!A:L',
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        print(f"✅ Saved {len(qualified_leads)} leads to Google Sheets")
        return True
    
    except Exception as e:
        print(f"❌ Error saving to sheets: {e}")
        return False


def get_sheet_url():
    """Return the Google Sheet URL."""
    if SHEET_ID:
        return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
    return None