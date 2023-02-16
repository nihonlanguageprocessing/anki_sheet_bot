from anki_param_parser import get_idx, get_note
from google_sheet import get_anki_params, google_sheets, move_values
from google_service import get_service
from anki_api import invoke, upload


## to do, create ability to read row 1, 1, return error message
if __name__ == '__main__':
    spreadsheet_id = '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk'
    sheet_id_from = 64971627
    sheet_id_to = 0

    service = get_service()

    header, range_, notes = google_sheets(service, get_anki_params, spreadsheet_id, sheet_id_from)

    note_idx = get_idx(header)

    success = []
    failure = []
    for row_idx, note_ in enumerate(notes):
        note = get_note(note_idx, note_)
        result = upload(note=note)
        if result is True:
            success.append(note_)
        else:
            failure.append(note_)
    if len(success) > 0:
        google_sheets(service, move_values, '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk',sheet_id_from, sheet_id_to, range_, success)
    if len(failure) > 0:
        google_sheets(service, move_values, '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk',sheet_id_from, sheet_id_from, range_, failure)



    #result = invoke("sync")
    print(success)
    print(failure)



##get data
##send to
