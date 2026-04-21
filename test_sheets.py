from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

print(f"Testing Google Sheets...")
print(f"Sheet ID: {SHEET_ID}")

if not SHEET_ID:
    print("❌ GOOGLE_SHEET_ID not found in .env")
    exit(1)

try:
    print("🔄 Initializing Sheets API...")
    creds = Credentials.from_service_account_file(
        'google_credentials.json',
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    print("✅ Credentials loaded!")
    
    print("🔄 Testing API connection...")
    result = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheet_title = result['properties']['title']
    print(f"✅ Connected to sheet: '{sheet_title}'")
    
    print("🔄 Writing test data...")
    test_data = [
        ['Test', 'Data', 'Row'],
        ['Hello', 'Google', 'Sheets']
    ]
    
    body = {'values': test_data}
    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range='Sheet1!A:C',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    print("✅ Test data written successfully!")
    
    print(f"\n🎉 Google Sheets is working!")
    print(f"📊 Open your sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    
except FileNotFoundError:
    print("❌ google_credentials.json not found!")
except Exception as e:
    print(f"❌ Error: {e}")