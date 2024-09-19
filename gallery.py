from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
creds = Credentials.from_service_account_file(
    'credentials.json', scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)


class Gallery:
    def __init__(self, parent_folder_id):
        self.parent_folder_id = parent_folder_id

    def get_categories(self) -> dict[str, list[dict[str, str]]]:
        r"""
        Get all the folders in the parent folder and their images.

        Returns:
        dict[str, list[dict[str, str]]]: A dictionary where the key is the folder name and the value is a list of dictionaries containing the image details.

        Example:
            {
                'Folder 1': [
                    {'src': 'https://drive.google.com/uc?id=1_vDkfinUuyvOXi0-fzBzUnUGhwmhsshq', 'alt': 'Image 1', 'name': 'Image 1', 'size': '1.23 MB'},
                    {'src': 'https://drive.google.com/uc?id=1_vDkfinUuyvOXi0-fzBzUnUGhwmhsshq', 'alt': 'Image 2', 'name': 'Image 2', 'size': '1.23 MB'}
                ],
                'Folder 2': [
                    {'src': 'https://drive.google.com/uc?id=1_vDkfinUuyvOXi0-fzBzUnUGhwmhsshq', 'alt': 'Image 4', 'name': 'Image 4', 'size': '1.23 MB'},
                    {'src': 'https://drive.google.com/uc?id=1_vDkfinUuyvOXi0-fzBzUnUGhwmhsshq', 'alt': 'Image 5', 'name': 'Image 5', 'size': '1.23 MB'}
                ]
            }
        """
        query = f"'{
            self.parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"

        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        gallery = {}

        if not folders:
            print("No folders found.")
        else:
            for folder in folders:
                gallery[folder['name']] = self.get_images(folder['id'])

        return gallery

    def get_images(self, parent_folder_id: str) -> list[dict[str, str]]:
        r"""
        Get all the images in the folder.

        Args:
        parent_folder_id (str): The ID of the parent folder.
        """

        query = f"'{
            parent_folder_id}' in parents and (mimeType contains 'image/') and trashed = false"

        results = service.files().list(
            q=query, fields="files(id, name, mimeType, size, description)").execute()
        images = results.get('files', [])
        data = []

        if not images:
            print("No images found.")
        else:
            for image in images:
                tmp = {}
                tmp['src'] = f"https://drive.google.com/uc?id={image['id']}"
                tmp['alt'] = image['name']
                tmp['name'] = image['name']
                description = image.get(
                    'description', 'No description available')

                print(f" - Description: {description}")

                size = image.get('size', 'Unknown')
                if size != 'Unknown':
                    size = int(size)
                    if size >= 1024 * 1024:
                        size = f"{size / (1024 * 1024):.2f} MB"
                    elif size >= 1024:
                        size = f"{size / 1024:.2f} KB"
                    else:
                        size = f"{size} B"
                tmp['size'] = size

                data.append(tmp)

        return data


