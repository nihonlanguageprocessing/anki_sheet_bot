import json
import urllib.request

ACTION = 'action'
VERSION = 6

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

if __name__ == "__main__":
    invoke('createDeck', deck='test1')
    result = invoke('deckNames')
    print('got list of decks: {}'.format(result))


'''
(*.jpg *.png *.gif *.tiff *.svg *.tif *.jpeg "+ "*.mp3 *.ogg *.wav *.avi *.ogv *.mpg *.mpeg *.mov *.mp4 " + "*.mkv *.ogx *.ogv *.oga *.flv *.swf *.flac *.webp *.m4a)")
'''
'''
{
    "action": "addNotes",
    "version": 6,
    "params": {
        "notes": [
            {
                "deckName": "Default",
                "modelName": "Basic",
                "fields": {
                    "Front": "front content",
                    "Back": "back content"
                },
                "tags": [
                    "yomichan"
                ],
                "audio": [{
                    "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                    "filename": "yomichan_ねこ_猫.mp3",
                    "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                    "fields": [
                        "Front"
                    ]
                }],
                "video": [{
                    "url": "https://cdn.videvo.net/videvo_files/video/free/2015-06/small_watermarked/Contador_Glam_preview.mp4",
                    "filename": "countdown.mp4",
                    "skipHash": "4117e8aab0d37534d9c8eac362388bbe",
                    "fields": [
                        "Back"
                    ]
                }],
                "picture": [{
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/A_black_cat_named_Tilly.jpg/220px-A_black_cat_named_Tilly.jpg",
                    "filename": "black_cat.jpg",
                    "skipHash": "8d6e4646dfae812bf39651b59d7429ce",
                    "fields": [
                        "Back"
                    ]
                }]
            }
        ]
    }
}'''
