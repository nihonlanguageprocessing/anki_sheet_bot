from anki_param_parser import get_idx, get_note
from google_sheet import get_anki_params, google_sheets
from google_service import get_service
from anki_api import invoke


## to do, create ability to read row 1, 1, return error message
if __name__ == '__main__':
    spreadsheet_id = '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk'
    sheet_id_from = 64971627

    service = get_service()

    header, _, notes = google_sheets(service, get_anki_params, spreadsheet_id, sheet_id_from)

    idx = get_idx(header)


    for note_ in notes:
        note = get_note(idx, note_)
        try:
            result = invoke('addNote', note=note)
            print(result)

        except Exception as e:
            print(e)
            print(notes)

    result = invoke("sync")





##get data
##send to
