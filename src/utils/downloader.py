import requests
from .encryption import decrypt_zip


def download_file(url: str, local_path: str):
    response = requests.get(url)
    with open(local_path, "wb") as file:
        file.write(response.content)

def download_encrypted_zip(url: str, local_file_path: str, extract_to_path: str, key: str):
    response = requests.get(url)
    with open(local_file_path, "wb") as file:
        file.write(response.content)

    decrypt_zip(local_file_path, extract_to_path, key)