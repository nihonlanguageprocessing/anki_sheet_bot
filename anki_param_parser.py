from google_sheet import get_anki_params, google_sheets
from google_service import get_service
import os

# TO DO

# put it all together
# Get delin from .ini
# how to handle that if there is a url there has to be a file name? Params that are required together??
# how to limit certain params to certain values

DELIN = ','
DEFAULT_DECK = 'Default'
DEFAULT_MODEL = 'Basic'
AUDIO= ('.mp3','.ogg','.wav','.avi','.ogv','.mpg','.mpeg','.mov','.mp4')
MOVIE= ('.mkv','.ogx','.ogv','.oga','.flv','.swf','.flac','.webp','.m4a')
PICTURE= ('.jpg','.png','.gif','.tiff','.svg','.tif','.jpeg')

def parse_core_idx(header: list) -> tuple:
    '''Returns idx for core params'''
    params = ('deckName','modelName')

    ## Deckname can be a parameter for multiple fields.
    core_idx = multi_param_idx_finder(header, params=params, start=0, end=2)
    return core_idx

def get_core(core_idx: list, note) -> dict:
    '''Returns any media compenents of a single anki note in the
    correct dictionary form'''
    core = {}

    (deck_name_idx, model_name_idx) = core_idx
    if deck_name_idx is not None and value_exists(note, deck_name_idx):
        core["deckName"] = note[deck_name_idx]
    else:
        core["deckName"] = DEFAULT_DECK
    if model_name_idx and value_exists(note, model_name_idx):
        core["modelName"] = note[model_name_idx]
    else:
        core["modelName"] = DEFAULT_MODEL

    return core

def parse_options_idx(header: list) -> list:
    '''Returns idx for options params'''
    params = ('allowDuplicate','duplicateScope'
              ,'deckName','checkChildren','checkAllModels')

    options_idx = multi_param_idx_finder(header, params=params, start=1)
    return options_idx

def get_options(options_idx: list, note):
    '''Returns any options compenents of a single anki note in the
    correct dictionary form'''
    options = {}
    (allowDup_idx, dupScope_idx, deckName_idx, checkChil_idx, checkAllMod_idx) = options_idx
    if allowDup_idx and value_exists(note, allowDup_idx):
        options["allowDuplicate"] = note[allowDup_idx]
    if dupScope_idx and value_exists(note, dupScope_idx):
        options["duplicateScope"] = note[dupScope_idx]
    if deckName_idx or checkChil_idx or checkAllMod_idx:
        options['duplicateScopeOptions'] = {}
        if deckName_idx and value_exists(note, deckName_idx):
            options['duplicateScopeOptions']['deckName'] = note[deckName_idx]
        if checkChil_idx and value_exists(note, checkChil_idx):
            options['duplicateScopeOptions']['checkChildren'] = note[checkChil_idx]
        if checkAllMod_idx and value_exists(note, checkAllMod_idx):
            options['duplicateScopeOptions']['checkAllModels'] = note[checkAllMod_idx]

    return options

def parse_media_idx(header) -> list:
    '''Returns idx for media params. One list for each media item.'''
    start = 0
    medias_idx = []

    params = ('filename', 'skipHash', 'fields')
    # Finds the idx of first and second (if exists) 'url' components.
    # Used as limits for finding idx of other components.
    url_idx = index_of("url", header, start)
    url_idx_2 = index_of("url", header, url_idx+1)

    # Continues going through the header until all possible media components
    # have been exhausted.
    while url_idx:
        # Gets idx for any other named parameters corresponding to this url
        media_sub_idx = multi_param_idx_finder(header,
                                        params=params,
                                        start=url_idx, end=url_idx_2)

        # Append list of corresponding media params
        medias_idx.append([url_idx] + media_sub_idx)
        # Find idx of next 'url' component
        if url_idx_2:
            url_idx = index_of("url", header, url_idx_2)
            if url_idx:
                url_idx_2 = index_of("url", header, url_idx+1)
        # If already at end of header, exit.
        else:
            break

    return medias_idx

def get_media(medias_idx: list, note) -> list:
    '''Returns any media compenents of a single anki note in the
    correct dictionary form'''
    # Continues going through the header until all possible media components
    # have been exhausted.
    medias = {}

    for media_idx in medias_idx:
        media = {}
        # Gets idx for any other named parameters corresponding to this url
        (url_idx, filename_idx, skipHash_idx, fields_idx) = media_idx

        # add corresponding not values to dict
        if url_idx and value_exists(note, url_idx):
            media["url"] = note[url_idx]
        if skipHash_idx and value_exists(note, skipHash_idx):
            media["skipHash"] = note[skipHash_idx]
        if fields_idx and value_exists(note, fields_idx):
            media["fields"] = [field.strip() for field in note[fields_idx].split(DELIN)]
        if filename_idx and value_exists(note, filename_idx):
            media["fileName"] = note[filename_idx]
            type_ = get_media_type(media["filename"])
            medias[type_] = media



        # append dict to list of medias


    return medias

def get_media_type(file_name) -> str:
    '''Gets media type from the file name of the media'''
    _, file_type = os.path.splitext(file_name)
    if file_type in AUDIO:
        return 'audio'
    if file_type in MOVIE:
        return 'movie'
    if file_type in PICTURE:
        return 'picture'
    pass

def parse_fields_idx(header, core_idx, options_idx, media_idx):
    '''Returns idx for options params.

    These are not named.
    All idx between core and media / options are field params.'''

    # Get left idx based on how many core idx exists
    left_idx = max([_ for _ in core_idx + [-1] if _ is not None]) + 1

    # Get right idx. If no options or media_idx, set the right idx as the len of
    # the header
    right_idx = min([_ for _ in options_idx + sum(media_idx,[]) if _ is not None])
    if right_idx:
        right_idx
    else:
        right_idx = len(header)
    return list(range(left_idx, right_idx))

def get_field_names(header: list, fields_idx:list) -> list:
    '''Returns a list of field names'''
    field_names_idx = [header[idx] for idx in fields_idx]
    return field_names_idx

def get_fields(field_idx: list, field_names: list, note: list) -> dict:
    '''Returns any field compenents of a single anki note in dictionary form'''
    fields = {}
    for name_idx, note_idx in enumerate(field_idx):
        if value_exists(note, note_idx):
            fields[field_names[name_idx]] = note[note_idx]
    return {"fields": fields}

def multi_param_idx_finder(header: list, params: tuple, start:int=0, end:int=0) -> list:
    '''Finds idx of a tuple of params'''
    idxs = []
    for param in params:
        idxs.append(index_of(param, header, start, end))
    return idxs


def index_of(note, list_, start=0, end=None):
    try:
        if end:
            return list_.index(note, start, end)
        return list_.index(note, start)
    except ValueError:
        return None
    except TypeError:
        return None

def value_exists(note:list, idx: int) -> bool:
    try:
        val = note[idx]
        if val != '':
            return True
        else:
            return False
    except IndexError:
        return False

def get_idx(header: list) -> list:
    media_idx = parse_media_idx(header)
    options_idx = parse_options_idx(header)
    core_idx = parse_core_idx(header)
    fields_idx = parse_fields_idx(header, core_idx, options_idx, media_idx)
    fields_names = get_field_names(header, fields_idx)

    return (media_idx, options_idx, core_idx, fields_idx, fields_names)

def get_note(idx: tuple, note: list) -> dict:
    (media_idx, options_idx, core_idx, fields_idx, fields_names) = idx

    note_dict = {}

    media = get_media(media_idx, note)
    options = get_options(options_idx, note)
    core = get_core(core_idx, note)
    fields = get_fields(fields_idx, fields_names, note)

    note_dict = core | fields | options | media

    return note_dict

if __name__ == "__main__":
    spreadsheet_id = '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk'
    sheet_id_from = 64971627

    service = get_service()

    header, _, notes = google_sheets(service, get_anki_params, spreadsheet_id, sheet_id_from)

    idx = get_idx(header)
    note = get_note(idx, notes[0])
    print(note)
