from __future__ import print_function

from googleapiclient.errors import HttpError
from google_service import get_service

def google_sheets(function_, *args):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """


    # pylint: disable=maybe-no-member
    try:
        service = get_service()
        value = function_(service, *args)
        return value

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def get_values(service, spreadsheet_id, sheet_ID, range_name):
    result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return
    return values

def write_values(spreadSheetID, sheetID, range):
    pass

def del_values(spreadSheetID, sheetID, range):
    pass

def get_sheetName(service, spreadsheet_id, sheet_id):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    for sheet in sheets:
        properties = sheet.get("properties")
        print(sheet)
        if properties.get('sheetId') == sheet_id:
            sheet_name = properties.get('title')
    return sheet_name

if __name__ == '__main__':
    # Pass: spreadsheet_id, and range_name
    sheet_name = google_sheets(get_sheetName, '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk', 64971627)
    print(sheet_name)
