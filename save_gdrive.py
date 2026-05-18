import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def save_to_gdrive(from_path, names_list):
    # 1. Dynamically locate the JSON credentials file next to this script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CREDENTIALS_FILE = os.path.join(BASE_DIR, "gdive-api-theyafen.json")

    # 2. Authenticate with Google Drive
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    # 3. Define the file to upload and target Google Drive folder ID
    FOLDER_ID = "1qf5H2pYH_TM_adoCadLuUUjPAt7d3fw6"
    for file in names_list:
        file_to_upload = os.path.join(BASE_DIR, from_path, file)
        if os.path.exists(file_to_upload):
            print(f"Found file to upload: {file_to_upload}")
        else:
            print(f"File not found: {file_to_upload}")
            continue
    files_to_upload = os.path.join(BASE_DIR, from_path, names_list[0])

    # 4. Prepare metadata and upload
    file_metadata = {
        "name": "Monthly_Report.csv",
        "parents": [FOLDER_ID]
    }
    media = MediaFileUpload(file_to_upload, mimetype="application/pdf")

    uploaded_file = service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()

    print(f"File uploaded successfully! File ID: {uploaded_file.get('id')}")
