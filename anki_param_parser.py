from google_sheet import get_anki_params, google_sheets
from google_service import get_service
import os

# TO DO
# Get delin from .ini
# Rewrite media_param_idx_finder to take a list of params

DELIN = ','
AUDIO= ('.mp3','.ogg','.wav','.avi','.ogv','.mpg','.mpeg','.mov','.mp4')
MOVIE= ('.mkv','.ogx','.ogv','.oga','.flv','.swf','.flac','.webp','.m4a')
PICTURE= ('.jpg','.png','.gif','.tiff','.svg','.tif','.jpeg')

def core_parser(header):
    deck_name_idx = index_of("deckName", header)
    model_name_idx = index_of("modelName", header)

def parse_options_idx(header) -> list:
    '''Returns idx for options params'''
    params = ('allowDuplicate','duplicateScope'
              ,'deckName','checkChildren','checkAllModels')

    options_idx = multi_param_idx_finder(header, params=params, start=1)
    return options_idx

def get_options(options_idx: list, note):
    '''Returns dictionary of options params and their values for a given note'''
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
    '''Parse any media compenents of a header and single anki note into the
    correct dictionary form'''
    # Continues going through the header until all possible media components
    # have been exhausted.
    medias = []

    for media_idx in medias_idx:
        media = {}
        # Gets idx for any other named parameters corresponding to this url
        (url_idx, filename_idx, skipHash_idx, fields_idx) = media_idx

        # add corresponding not values to dict
        media['url'] = note[url_idx]
        media["filename"] = note[filename_idx]
        type_ = get_media_type(media["filename"])
        if skipHash_idx:
            media["skipHash"] = note[skipHash_idx]
        if fields_idx:
            media["fields"] = [field.strip() for field in note[fields_idx].split(DELIN)]


        # append dict to list of medias
        medias.append({'type': type_, 'media': media})

    return medias

def get_media_type(file_name) -> str:
    _, file_type = os.path.splitext(file_name)
    if file_type in AUDIO:
        return 'audio'
    if file_type in MOVIE:
        return 'movie'
    if file_type in PICTURE:
        return 'picture'
    pass

def multi_param_idx_finder(header: list, params: tuple, start:int=0, end:int=0) -> list:
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

    media_idx = parse_media_idx(header)
    media = get_media(media_idx, notes[0])
    print(media)
