import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = "payslips"

CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_files_to_upload():
    files_to_upload = []

    print(f"Looking for files to upload in: {os.path.join(BASE_DIR, SAVE_DIR)}")
    for file in os.listdir(os.path.join(BASE_DIR, SAVE_DIR)):
        if file.endswith(".pdf"):
            files_to_upload.append(file)
            print(f"Found file to upload: {file}")

    return files_to_upload


def get_drive_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"OAuth credentials file not found: {CREDENTIALS_FILE}. "
                    "Create an OAuth client ID in Google Cloud Console and save it as credentials.json."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            if not flow.redirect_uri:
                flow.redirect_uri = flow.client_config.get("redirect_uris", [None])[0]
            if not flow.redirect_uri:
                raise ValueError(
                    "OAuth client does not have a redirect URI. "
                    "Use a Desktop app OAuth client or add a localhost redirect URI to the credentials."
                )
            try:
                print("Starting local authorization server on WSL. If the browser does not open, copy the shown URL into your browser.")
                creds = flow.run_local_server(host="0.0.0.0", port=0, open_browser=False)
            except Exception:
                print("Could not start the local callback server. Falling back to manual authorization.")
                auth_url, _ = flow.authorization_url(prompt="consent")
                print("Please open this URL in your browser and authorize the application:")
                print(auth_url)
                code = input("Enter the authorization code: ").strip()
                flow.fetch_token(code=code)
                creds = flow.credentials
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return creds


def save_to_gdrive():
    print("Starting Google Drive upload process...")

    creds = get_drive_credentials()
    service = build("drive", "v3", credentials=creds)

    # 3. Define the file to upload and target Google Drive folder ID
    # Use a folder ID from your personal Drive or a shared folder you own.
    FOLDER_ID = "YOUR_PERSONAL_DRIVE_FOLDER_ID_HERE"

    print(f"Looking for files to upload in: {os.path.join(BASE_DIR, SAVE_DIR)}")
    files_to_upload = get_files_to_upload()
    print(f"Files to upload: {files_to_upload}")

    for file in files_to_upload:
        file_to_upload = os.path.join(BASE_DIR, SAVE_DIR, file)
        if not os.path.exists(file_to_upload):
            print(f"File not found: {file_to_upload}")
            continue

        print(f"Uploading file: {file_to_upload}")
        file_metadata = {
            "name": file,
            "parents": [FOLDER_ID]
        }
        media = MediaFileUpload(file_to_upload, mimetype="application/pdf")

        uploaded_file = service.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()
        print(f"File uploaded successfully! File ID: {uploaded_file.get('id')}")
