from google_sheet import get_anki_params, google_sheets
from google_service import get_service

# TO DO
# Get delin from .ini
# Rewrite media_param_idx_finder to take a list of params

DELIN = ','

def core_parser(header):
    deck_name_idx = index_of("deckName", header)
    model_name_idx = index_of("modelName", header)

def options_parser(header, values):
    pass
    '''         "options": {
                "allowDuplicate": false,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": false,
                    "checkAllModels": false
                }
            },'''



def media_parser(header, value) -> list:
    '''Parse any media compenents of a header and single anki note into the
    correct dictionary form'''
    start = 0
    media = []

    # Finds the idx of first and second (if exists) 'url' components.
    # Used as limits for finding idx of other components.
    url_idx = index_of("url", header, start)
    url_idx_2 = index_of("url", header, url_idx+1)

    # Continues going through the header until all possible media components
    # have been exhausted.
    while url_idx:
        # Gets idx for any other named parameters corresponding to this url
        filename_idx, skipHash_idx, fields_idx = multi_param_idx_finder(header,
                                        params=('filename', 'skipHash', 'fields'),
                                        start=url_idx, end=url_idx_2)

        # Append a new dictionary and add corresponding values
        media.append({})
        media[-1]['url'] = value[url_idx]
        if filename_idx:
            media[-1]["filename"] = value[filename_idx]
        if skipHash_idx:
            media[-1]["skipHash"] = value[skipHash_idx]
        if fields_idx:
            media[-1]["fields"] = [field.strip() for field in value[fields_idx].split(DELIN)]

        # Find idx of next 'url' component
        if url_idx_2:
            url_idx = index_of("url", header, url_idx_2)
            if url_idx:
                url_idx_2 = index_of("url", header, url_idx+1)
        # If already at end of header, exit.
        else:
            break

    return media

def media_param_idx_finder(header, start=0, end=0, include_url=False) -> tuple:
    '''Finds idx of any named parameters for media files.

    By default this will not include the idx of url
    it will include 'filename', 'skipHash', 'fields'. '''
    url_idx = index_of("url", header, start, end)
    filename_idx = index_of("filename", header, start, end)
    skipHash_idx = index_of("skipHash", header, start, end)
    fields_idx = index_of("fields", header, start, end)

    if include_url:
        url_idx = index_of("url", header, start, end)
        return (url_idx, filename_idx, skipHash_idx, fields_idx)
    return (filename_idx, skipHash_idx, fields_idx)

def multi_param_idx_finder(header: list, params: list, start:int=0, end:int=0):
    idxs = []
    for param in params:
        idxs.append(index_of(param, header, start, end))
    return idxs


def fields_parser(headers, value):
    #last_idx = skipHash_idx or filename_idx or url_idx
    #first_idx = url_idx_2 or (len_-1)
    #    if first_idx - last_idx > 1:
    #        fields = value[last_idx+1: first_idx]
    #        media[-1]["fields"] = fields
    pass

def index_of(value, list_, start=0, end=None):
    try:
        if end:
            return list_.index(value, start, end)
        return list_.index(value, start)
    except ValueError:
        return None
    except TypeError:
        return None


if __name__ == "__main__":
    spreadsheet_id = '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk'
    sheet_id_from = 64971627

    service = get_service()

    header, _, values = google_sheets(service, get_anki_params, spreadsheet_id, sheet_id_from)

    media = media_parser(header, values[0])
    print(media)
