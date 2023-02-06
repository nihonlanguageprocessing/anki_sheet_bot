from google_sheet import get_anki_params, google_sheets
from google_service import get_service


def field_parser(header):
    deck_name_idx = index_of("deckName", header)
    model_name_idx = index_of("modelName", header)

def media_param_idx_finder(header, start=0, end=0):
    url_idx = index_of("url", header, start, end)
    filename_idx = index_of("filename", header, start, end)
    skipHash_idx = index_of("skipHash", header, start, end)

    return (url_idx, filename_idx, skipHash_idx)

def media_parser(header, value):
    len_ = len(values)
    start = 0
    media = [{}]
    url_idx = index_of("url", header, start)
    url_idx_2 = index_of("url", header, url_idx+1)
    while url_idx:
        media[-1]['url'] = value[url_idx]
        url_idx, filename_idx, skipHash_idx = media_param_idx_finder(header, url_idx, url_idx_2)
        if filename_idx:
            media[-1]["filename"] = value[filename_idx]
        if skipHash_idx:
            media[-1]["skipHash"] = value[skipHash_idx]

        last_idx = skipHash_idx or filename_idx or url_idx
        first_idx = url_idx_2 or (len_-1)
        if first_idx - last_idx > 1:
            fields = value[last_idx+1: first_idx]
            media[-1]["fields"] = fields
        print(media)

        if url_idx_2:
            url_idx = index_of("url", header, url_idx_2)
            if url_idx:
                url_idx_2 = index_of("url", header, url_idx+1)
                media.append({})
        else:
            break

    return media


def index_of(value, list_, start=0, end=None):
    try:
        if end:
            return list_.index(value, start, end)
        return list_.index(value, start)
    except ValueError:
        return None
    except TypeError:
        return None

'''
                "audio": [{
                    "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                    "filename": "yomichan_ねこ_猫.mp3",
                    "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                    "fields": [
                        "Front"
                    ]
'''

if __name__ == "__main__":
    spreadsheet_id = '1Vh8IB6pyUSgff-SaTmsIrOsTlrL8-NQGtlil_FhOrIk'
    sheet_id_from = 64971627

    service = get_service()

    header, _, values = google_sheets(service, get_anki_params, spreadsheet_id, sheet_id_from)

    media = media_parser(header, values[0])
    print(media)
