from google.oauth2.credentials import Credentials
import json
import os

TOKEN_FILE = "token_store.json"

# Load stored tokens
def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        return {}
    with open(TOKEN_FILE, "r") as file:
        return json.load(file)

# Authenticate user using their stored token
def authenticate_drive(user_id):
    tokens = load_tokens()
    user_id = str(user_id)

    if user_id not in tokens:
        raise Exception("User not authenticated. Use /auth <credtoken> to authenticate.")

    # Load user-specific credentials
    credentials = Credentials.from_authorized_user_info(json.loads(tokens[user_id]))
    return build("drive", "v3", credentials=credentials)

# Upload file to Google Drive
def upload_to_drive(user_id, file_path, file_name):
    service = authenticate_drive(user_id)
    file_metadata = {"name": file_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    return file.get("id")
