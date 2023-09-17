from google.oauth2 import service_account
from googleapiclient.discovery import build
from docarray import DocArray
from typing import Optional

# Google Drive API settings
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE: str = 'path/to/service_account_credentials.json'  # Update with your service account credentials file path
DRIVE_FILE_ID: str = 'your_drive_file_id'  # Update with your CSV file's ID in Google Drive

# DocArray settings
DB_PATH: str = 'your_database_path'


def import_csv_from_google_drive() -> DocArray:
    # Authenticate with Google Drive API
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)

    # Download the CSV file from Google Drive
    request = drive_service.files().get_media(fileId=DRIVE_FILE_ID)
    downloader = request.execute()

    # Load the downloaded data into a DocArray object
    doc_array = DocArray(downloader)

    return doc_array


def save_docarray_to_datastore(doc_array: DocArray, datastore_path: str) -> None:
    # Save the DocArray to the datastore
    doc_array.save(datastore_path)

    print("DocArray data saved to the persistent datastore.")


# Usage example
def main() -> None:
    service_account_credentials: str = 'path/to/service_account_credentials.json'
    datastore_path: str = 'your_database_path'

    try:
        # Fetch the CSV data as DocArray
        doc_array = import_csv_from_google_drive()

        # Save the DocArray to the persistent datastore
        save_docarray_to_datastore(doc_array, datastore_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
