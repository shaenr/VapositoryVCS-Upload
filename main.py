from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from pathlib import Path

VIDEO_URL = Path('/media/shaen/Home/zips/METAPRISE APPLICATIONS & b l u e s c r e e n - Cruisesoft/output.mkv')

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


def initialize_upload(service):
    # publish_date_time = datetime.datetime(2022, 2, 6, 9, 30, 0).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'categoryId': MUSIC_CATEGORY_ID,
            'title': "Metaprise Applications - Island Port Arrival",
            'description': 'This is a vaporwave video by Metaprise Applications',
            'tags': ['vaporwave']
        },
        'status': {
            'privacyStatus': 'private',
            # 'publishAt': publish_date_time,
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': False
    }

    media_body = MediaFileUpload(VIDEO_URL, chunksize=-1, resumable=True)

    upload = service.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_body
    ).execute()

    # resumable_upload(upload)


# def resumable_upload(insert_request):
#     response = None
#     error = None
#     retry = 0
#     while response is None:
#         try:
#             print("Uploading file...")
#             status, response = insert_request
#             if response is not None:
#                 if 'id' in response:
#                     print(f"Video id {response['id']} was successfully uploaded.")
#                 else:
#                     sys.exit(f"The upload failed with unexpected response: {response}")
#         except HttpError as e:
#             if e.resp.status in RETRIABLE_STATUS_CODES:
#                 error = f"A retriable HTTP error {e.resp.status} occurred: {e.content}"
#             else:
#                 raise
#
#         if error is not None:
#             print(error)
#             retry += 1
#             if retry > MAX_RETRIES:
#                 sys.exit("No longer attempting to retry")
#
#             max_sleep = 2 ** retry
#             sleep_seconds = random.random() * max_sleep
#             print(f"Sleeping for {sleep_seconds} and then retrying...")
#             time.sleep(sleep_seconds)


if __name__ == '__main__':
    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube)
    except HttpError as e:
        print(f"An HTTP Error occurred: {e.resp.status}: {e.content}")
