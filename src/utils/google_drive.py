import os
import pickle
import base64
import pandas as pd

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
from googleapiclient.http import (
    MediaFileUpload,
    MediaIoBaseDownload
)

# ==========================
# Config
# ==========================

LOCAL_CLIENT_SECRET = r"C:\Users\Pasha\Desktop\Downloads\client_secret.json"

CLIENT_SECRET_FILE = "client_secret.json"

TOKEN_FILE = "token.pickle"

FOLDER_ID = "1vaROMgv0MV3j96InibaUXY3PWANuk449"

SCOPES = [
    "https://www.googleapis.com/auth/drive"
]

# ==========================
# GitHub Detection
# ==========================

def running_on_github():

    return os.getenv("GITHUB_ACTIONS") == "true"


# ==========================
# Build local auth files from GitHub Secrets
# ==========================

def prepare_github_credentials():

    if not running_on_github():
        return

    if not os.path.exists(CLIENT_SECRET_FILE):

        secret = os.getenv("GOOGLE_CLIENT_SECRET")

        if not secret:
            raise Exception("GOOGLE_CLIENT_SECRET not found")

        with open(
            CLIENT_SECRET_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(secret)

    if not os.path.exists(TOKEN_FILE):

        token = os.getenv("GOOGLE_TOKEN_PICKLE")

        if not token:
            raise Exception("GOOGLE_TOKEN_PICKLE not found")

        with open(
            TOKEN_FILE,
            "wb"
        ) as f:

            f.write(
                base64.b64decode(token)
            )


# ==========================
# Google Drive Connection
# ==========================

def get_drive_service():

    prepare_github_credentials()

    creds = None

    if os.path.exists(TOKEN_FILE):

        with open(
            TOKEN_FILE,
            "rb"
        ) as token:

            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            secret_file = (
                CLIENT_SECRET_FILE
                if running_on_github()
                else LOCAL_CLIENT_SECRET
            )

            flow = InstalledAppFlow.from_client_secrets_file(
                secret_file,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open(
            TOKEN_FILE,
            "wb"
        ) as token:

            pickle.dump(
                creds,
                token
            )

    return build(
        "drive",
        "v3",
        credentials=creds
    )


# ==========================
# Find File
# ==========================

def find_file(filename):

    service = get_drive_service()

    query = (
        f"'{FOLDER_ID}' in parents "
        f"and name='{filename}' "
        f"and trashed=false"
    )

    result = service.files().list(
        q=query,
        fields="files(id,name)"
    ).execute()

    files = result.get(
        "files",
        []
    )

    if files:
        return files[0]["id"]

    return None


# ==========================
# Upload File
# ==========================

def upload_file(local_path, filename):

    service = get_drive_service()

    file_id = find_file(filename)

    media = MediaFileUpload(
        local_path,
        resumable=True
    )

    if file_id:

        service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()

        print(f"Updated: {filename}")

    else:

        metadata = {
            "name": filename,
            "parents": [FOLDER_ID]
        }

        service.files().create(
            body=metadata,
            media_body=media
        ).execute()

        print(f"Uploaded: {filename}")


# ==========================
# Download File
# ==========================

def download_file(filename, local_path):

    service = get_drive_service()

    query = (
        f"'{FOLDER_ID}' in parents "
        f"and name='{filename}' "
        f"and trashed=false"
    )

    result = service.files().list(
        q=query,
        fields="files(id,name)"
    ).execute()

    files = result.get(
        "files",
        []
    )

    if not files:

        print(f"File not found: {filename}")

        return False

    file_id = files[0]["id"]

    request = service.files().get_media(
        fileId=file_id
    )

    with open(
        local_path,
        "wb"
    ) as f:

        downloader = MediaIoBaseDownload(
            f,
            request
        )

        done = False

        while not done:

            status, done = downloader.next_chunk()

            if status:

                print(
                    f"Download {int(status.progress()*100)}%"
                )

    print(f"Downloaded: {filename}")

    return True


# ==========================
# Download Parquet
# ==========================

def download_parquet(filename="uk_jobs_master.parquet"):

    local_path = f"data/{filename}"

    os.makedirs(
        "data",
        exist_ok=True
    )

    success = download_file(
        filename,
        local_path
    )

    if not success:
        return None

    return pd.read_parquet(local_path)


# ==========================
# Upload Parquet
# ==========================

def upload_parquet(df, filename="uk_jobs_master.parquet"):

    local_path = f"data/{filename}"

    os.makedirs(
        "data",
        exist_ok=True
    )

    df.to_parquet(
        local_path,
        index=False
    )

    upload_file(
        local_path,
        filename
    )