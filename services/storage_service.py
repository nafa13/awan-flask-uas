import os
import uuid
from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def save_file(self, file_obj) -> str:
        """Menyimpan file dan mengembalikan URL/Path"""
        pass

class LocalStorageService(StorageService):
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        
    def save_file(self, file_obj) -> str:
        if not file_obj:
            return None
            
        ext = file_obj.filename.rsplit('.', 1)[1].lower()
        saved_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(self.upload_folder, saved_filename)
        
        file_obj.save(file_path)
        return saved_filename

class GCPStorageService(StorageService):
    """
    Placeholder untuk integrasi Google Cloud Storage Bucket.
    Akan diimplementasikan pada deployment fase 2.
    """
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        # self.client = storage.Client()
        
    def save_file(self, file_obj) -> str:
        if not file_obj:
            return None
            
        # ext = file_obj.filename.rsplit('.', 1)[1].lower()
        # blob_name = f"{uuid.uuid4().hex}.{ext}"
        # bucket = self.client.bucket(self.bucket_name)
        # blob = bucket.blob(blob_name)
        # blob.upload_from_file(file_obj)
        # return blob.public_url
        
        return "https://storage.googleapis.com/placeholder/image.jpg"
