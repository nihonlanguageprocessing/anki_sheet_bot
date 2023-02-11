from anki_param_parser import get_idx, get_note
from google_sheet import get_anki_params, google_sheets
from google_service import get_service
from anki_api import invoke

if __name__ == '__main__':
    spreadsheet_id = '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk'
    sheet_id_from = 64971627

    service = get_service()

    header, _, notes = google_sheets(service, get_anki_params, spreadsheet_id, sheet_id_from)

    idx = get_idx(header)
    note = get_note(idx, notes[0])
    print(note)

    #result = invoke('addNote', note=note)
    result = invoke("sync")

    print(result)



##get data
##send to
