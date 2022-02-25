from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from pathlib import Path
import json


def deserialize_json(p: str = "/media/shaen/Home/Digi,.json "):
    path = Path(p)
    with path.open('w') as fo:
        return json.load(fo)


VIDEO_URL = Path('')

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CREDENTIALS_PICKLE = Path('token.pickle')
CLIENT_SECRET_FILE = Path('client_secret.json')
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

MUSIC_CATEGORY_ID = 10


def get_authenticated_service():
    credentials = None

    if CREDENTIALS_PICKLE.exists():
        print("Loading Credentials From File")
        with CREDENTIALS_PICKLE.open('rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )

            flow.run_local_server(port=8080, prompt='consent',
                                  authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with CREDENTIALS_PICKLE.open('wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    return build(API_NAME, API_VERSION, credentials=credentials)


def initialize_upload(service, d):
    # publish_date_time = datetime.datetime(2022, 2, 6, 9, 30, 0).isoformat() + '.000Z'

    media_body = MediaFileUpload(VIDEO_URL, chunksize=-1, resumable=True)

    data = deserialize_json()

    tracks = data['tracks']['tracks']

    album_track_times = ""
    for idx, td in enumerate(tracks):
        album_track_times += f"{str(idx)}. {td['track']}  ({td['time']})\n"

    request_body = {
        'snippet': {
            'categoryId': MUSIC_CATEGORY_ID,
            'title': f"{data['ARTIST']} - {data['ALBUM_NAME']}",
            f"""
             ARTIST: {data['ARTIST']},
             ALBUM: {data['ALBUM_NAME']},
             DESCRIPTION: {data['ARTIST_BIO_TEXT']},
             DATE UPLOADED: {data['DATE_UPLOADED']},
             LOCATION: {data['LOCATION']},

             TRACK LIST: 
             {album_track_times}

             https://digi4.bandcamp.com/album/e-real-demo
             """
            'tags': [
                'electronic',
                'electronica',
                'future funk',
                'mallsoft',
                'vaporwave',
                'Czechia'
            ],
        },

        'status': {
            'privacyStatus': 'public',
            # 'publishAt': publish_date_time,
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': False
    }

    from pprint import pprint as pp
    pp(request_body)
    from sys import exit
    exit()

    # upload = service.videos().insert(
    #     part="snippet,status",
    #     body=request_body,
    #     media_body=media_body
    # ).execute()


if __name__ == '__main__':
    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube)
    except HttpError as e:
        print(f"An HTTP Error occurred: {e.resp.status}: {e.content}")
