import os
import uuid
import boto3
from botocore.exceptions import ClientError
from abc import ABC, abstractmethod
from flask import current_app

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

class CloudflareR2StorageService(StorageService):
    """
    Integrasi S3-Compatible Cloudflare R2 Object Storage.
    Memenuhi requirement EAS Cloud Computing.
    """
    def __init__(self):
        self.endpoint_url = current_app.config['R2_ENDPOINT']
        self.access_key = current_app.config['R2_ACCESS_KEY_ID']
        self.secret_key = current_app.config['R2_SECRET_ACCESS_KEY']
        self.bucket_name = current_app.config['R2_BUCKET_NAME']
        self.public_url = current_app.config['R2_PUBLIC_URL']
        
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='auto' # Cloudflare R2 uses 'auto'
        )
        
    def save_file(self, file_obj) -> str:
        if not file_obj:
            return None
            
        ext = file_obj.filename.rsplit('.', 1)[1].lower()
        blob_name = f"uploads/{uuid.uuid4().hex}.{ext}"
        
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                blob_name,
                ExtraArgs={'ContentType': file_obj.content_type}
            )
            # R2_PUBLIC_URL biasanya tidak berakhiran slash
            base_url = self.public_url.rstrip('/')
            return f"{base_url}/{blob_name}"
        except ClientError as e:
            current_app.logger.error(f"Gagal mengunggah ke R2: {e}")
            return None
