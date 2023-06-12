import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from ....pkg.config.config import config

UPLOAD_CONFIG = config["uploader"]

class GoogleDriveUploader:

    def __init__(self):
        creds = Credentials.from_service_account_file(UPLOAD_CONFIG["credentials"])
        self.service = build('drive', 'v3', credentials=creds)
        self.folder_id = UPLOAD_CONFIG["destination"]

    def get_metadata(self, media_path):
        return {
            'name': os.path.basename(media_path), 
            'parents': [self.folder_id]
        }

    def upload_and_get_link(self, media_path):
        media = MediaFileUpload(media_path)
        metadata = self.get_metadata(media_path)
        uploaded_file = self.service.files().create(body=metadata, media_body=media, fields='id').execute()
        file_id = uploaded_file['id']
        return f"https://drive.google.com/uc?export=preview&id={file_id}"
    
