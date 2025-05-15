import zipfile
import os

def decrypt_zip(zip_path: str, save_to: str, key: str):
    try:
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found at {zip_path}")
            
        if not os.path.exists(save_to):
            os.makedirs(save_to, exist_ok=True)
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            try:
                zip_ref.extractall(path=save_to, pwd=key.encode('utf-8'))
            except RuntimeError as e:
                if "Bad password" in str(e):
                    raise ValueError(f"Invalid password for zip file: {e}")
                raise e
    except zipfile.BadZipFile:
        raise ValueError(f"Invalid zip file format: {zip_path}")
    except Exception as e:
        raise e
