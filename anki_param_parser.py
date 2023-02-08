from google_sheet import get_anki_params, google_sheets
from google_service import get_service

# TO DO
# Get delin from .ini
# Rewrite media_param_idx_finder to take a list of params

DELIN = ','

def core_parser(header):
    deck_name_idx = index_of("deckName", header)
    model_name_idx = index_of("modelName", header)

def options_parser(header):
    params = ('allowDuplicate','duplicateScope'
              ,'deckName','checkChildren','checkAllModels')

    options_params_idx = multi_param_idx_finder(header, params=params, start=1)
    return options_param_idx

def options_getter(options_idx: tuple, note):
    options = {}
    (allowDup_idx, dupScope_idx, deckName_idx, checkChil_idx, checkAllMod_idx) = options_idx
    if allowDup_idx:
        options[-1]["allowDuplicate"] = note[allowDup_idx]
    if dupScope_idx:
        options[-1]["duplicateScope"] = note[dupScope_idx]
    if deckName_idx or checkChil_idx or checkAllMod_idx:
        options['duplicateScopeOptions'] = {}
        if deckName_idx:
            options['deckName'] = note[deckName_idx]
        if checkChil_idx:
            options['checkChildren'] = note[checkChil_idx]
        if checkAllMod_idx:
            options['checkAllModels'] = note[checkAllMod_idx]

    return options

def media_parser(header, note) -> list:
    '''Parse any media compenents of a header and single anki note into the
    correct dictionary form'''
    start = 0
    media = []

    params = ('filename', 'skipHash', 'fields')
    # Finds the idx of first and second (if exists) 'url' components.
    # Used as limits for finding idx of other components.
    url_idx = index_of("url", header, start)
    url_idx_2 = index_of("url", header, url_idx+1)

    # Continues going through the header until all possible media components
    # have been exhausted.
    while url_idx:
        # Gets idx for any other named parameters corresponding to this url
        filename_idx, skipHash_idx, fields_idx = multi_param_idx_finder(header,
                                        params=params,
                                        start=url_idx, end=url_idx_2)

        # Append a new dictionary and add corresponding notes
        media.append({})
        media[-1]['url'] = note[url_idx]
        if filename_idx:
            media[-1]["filename"] = note[filename_idx]
        if skipHash_idx:
            media[-1]["skipHash"] = note[skipHash_idx]
        if fields_idx:
            media[-1]["fields"] = [field.strip() for field in note[fields_idx].split(DELIN)]

        # Find idx of next 'url' component
        if url_idx_2:
            url_idx = index_of("url", header, url_idx_2)
            if url_idx:
                url_idx_2 = index_of("url", header, url_idx+1)
        # If already at end of header, exit.
        else:
            break

    return media


def multi_param_idx_finder(header: list, params: tuple, start:int=0, end:int=0):
    '''Finds idx of a tuple of params'''
    idxs = []
    for param in params:
        idxs.append(index_of(param, header, start, end))
    return idxs


def fields_parser(headers, note):
    #last_idx = skipHash_idx or filename_idx or url_idx
    #first_idx = url_idx_2 or (len_-1)
    #    if first_idx - last_idx > 1:
    #        fields = note[last_idx+1: first_idx]
    #        media[-1]["fields"] = fields
    pass

def index_of(note, list_, start=0, end=None):
    try:
        if end:
            return list_.index(note, start, end)
        return list_.index(note, start)
    except ValueError:
        return None
    except TypeError:
        return None


if __name__ == "__main__":
    spreadsheet_id = '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk'
    sheet_id_from = 64971627

    service = get_service()

    header, _, notes = google_sheets(service, get_anki_params, spreadsheet_id, sheet_id_from)

    media = media_parser(header, notes[0])
    print(media)
