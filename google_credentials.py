from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.json.

SERVICE_ACCOUNT_FILE = 'secret/sa_key.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

if __name__ == '__main__':
    get_credentials()
