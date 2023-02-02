from __future__ import print_function
from typing import List

from googleapiclient.errors import HttpError
from google_service import get_service

def google_sheets(service, function_, *args):
    # pylint: disable=maybe-no-member
    try:
        value = function_(service, *args)
        return value

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def get_values(service, spreadsheet_id, sheet_id, range_) -> List[List[str]]:
    range_name = google_sheets(service, get_rangeName, spreadsheet_id, sheet_id, range_)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return
    return values

def write_values(service, spreadsheet_id, sheet_id, range_, values) -> None:
    range_name = google_sheets(service, get_rangeName, spreadsheet_id, sheet_id, range_)
    body = {'values': values}
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED', insertDataOption = 'INSERT_ROWS', body=body).execute()
    pass

def del_values(service, spreadsheet_id, sheet_id, range_, values) -> None:
    range_name = google_sheets(service, get_rangeName, spreadsheet_id, sheet_id, range_)

    blank_values = [[''] * max(len(row) for row in values)] * len(values)
    body = {'values': blank_values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    pass

def move_values(service, spreadsheet_id, sheet_id_from, sheet_id_to, range_, values) -> None:
    google_sheets(service, write_values, spreadsheet_id, sheet_id_to, range_, values)
    google_sheets(service, del_values, spreadsheet_id, sheet_id_from, range_, values)
    pass

def get_sheetName(service, spreadsheet_id, sheet_id) -> str:
    sheet_metadata = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    for sheet in sheets:
        properties = sheet.get("properties")
        if properties.get('sheetId') == sheet_id:
            sheet_name = properties.get('title')
    if not sheet_name:
        print('No matching sheet found.')
        return
    return sheet_name

def get_rangeName(service, spreadsheet_id, sheet_id, range_) -> str:
    sheet_name = get_sheetName(service, spreadsheet_id, sheet_id)
    range_name = sheet_name + '!' + range_
    return range_name

if __name__ == '__main__':
    # Pass: spreadsheet_id, and range_name
    service = get_service()
    values = google_sheets(service, get_values, '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk', 64971627, 'A2:B')
    google_sheets(service, move_values, '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk',64971627, 0, 'A2:B', values)


    print(values)
