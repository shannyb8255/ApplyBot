import os
import re
import pickle
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Google Docs resume file ID from the URL
RESUME_DOC_ID = "1Cch_AXhouIONCkMuSi9U_bqz4OmbtWvxeO7zDHmu9Gk"

# Only read access to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def download_resume(creds):
    service = build('drive', 'v3', credentials=creds)

    # Get the file metadata (to access the title)
    metadata = service.files().get(fileId=RESUME_DOC_ID, fields='name').execute()
    doc_title = metadata['name']
    filename = f"{doc_title}.pdf"

    # Load last known version
    version_file = "last_version.txt"
    last_version = ""
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            last_version = f.read().strip()

    # If version is the same, skip download
    if doc_title == last_version:
        print(f"🟡 No update needed — '{doc_title}' is already the current version.")
        return

    # Save new version name
    with open(version_file, "w") as f:
        f.write(doc_title)

    # Make sure the archive folder exists
    archive_folder = "archive"
    os.makedirs(archive_folder, exist_ok=True)

    # Move old resume versions to archive
    for f in os.listdir():
        if re.match(r"Resume V \d+\.\d+\.pdf", f):
            shutil.move(f, os.path.join(archive_folder, f))
            print(f"📁 Moved old version to archive: {f}")

    # Export the Google Doc as a PDF
    request = service.files().export_media(fileId=RESUME_DOC_ID, mimeType='application/pdf')
    with open(filename, 'wb') as f:
        f.write(request.execute())

    print(f"✅ New resume titled '{doc_title}' downloaded and saved as '{filename}'.")

if __name__ == '__main__':
    creds = authenticate()
    download_resume(creds)
