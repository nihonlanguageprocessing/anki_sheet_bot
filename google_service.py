from googleapiclient.discovery import build
from google_credentials import get_credentials

def get_service():
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    return service

if __name__ == '__main__':
    get_service()
