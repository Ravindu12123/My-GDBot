from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def authenticate_drive():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("GDRIVE_CREDENTIALS_FILE"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("drive", "v3", credentials=creds)

def upload_to_drive(file_path, file_name):
    service = authenticate_drive()
    file_metadata = {"name": file_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    return file.get("id")
