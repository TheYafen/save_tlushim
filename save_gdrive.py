#!/mnt/c/TheYafen/scripts/save_tlushim/.venv/bin/python
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = "Payslips"

def get_files_to_upload():
    files_to_upload = []

    print(f"Looking for files to upload in: {os.path.join(BASE_DIR, SAVE_DIR)}")
    for file in os.listdir(os.path.join(BASE_DIR, SAVE_DIR)):
        if file.endswith(".pdf"):
            files_to_upload.append(file)
            print(f"Found file to upload: {file}")

    return files_to_upload

def save_to_gdrive():
    print("Starting Google Drive upload process...")
    # 1. Dynamically locate the JSON credentials file next to this script

    CREDENTIALS_FILE = os.path.join(BASE_DIR, "gdrive-api-theyafen.json")

    # 2. Authenticate with Google Drive
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    # 3. Define the file to upload and target Google Drive folder ID
    FOLDER_ID = "1qf5H2pYH_TM_adoCadLuUUjPAt7d3fw6"

    print(f"Looking for files to upload in: {os.path.join(BASE_DIR, SAVE_DIR)}")
    files_to_upload = get_files_to_upload()
    print(f"Files to upload: {files_to_upload}")

    for file in files_to_upload:

        file_to_upload = os.path.join(BASE_DIR, SAVE_DIR, file)
        if os.path.exists(file_to_upload):
            print(f"Found file to upload: {file_to_upload}")
        else:
            print(f"File not found: {file_to_upload}")
            continue

        # 4. Prepare metadata and upload
        file_metadata = {
            "name": file,
            "parents": [FOLDER_ID]
        }
        media = MediaFileUpload(file_to_upload, mimetype="application/pdf")

        uploaded_file = service.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()

        print(f"File uploaded successfully! File ID: {uploaded_file.get('id')}")
        break
