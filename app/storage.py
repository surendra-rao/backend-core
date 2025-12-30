import os
import shutil
from datetime import datetime, timedelta
from fastapi import UploadFile, HTTPException
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from . import config

# Initialize Azure Client (only if needed)
blob_service_client = None
if config.STORAGE_MODE == "azure":
    try:
        blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_CONN_STRING)
        try:
            blob_service_client.create_container(config.CONTAINER_NAME)
        except Exception:
            pass 
    except Exception as e:
        print(f"WARNING: Azure setup failed: {e}")

async def save_video(file: UploadFile):
    """Decides where to save the file based on config."""
    
    if config.STORAGE_MODE == "azure":
        # --- AZURE LOGIC ---
        if not blob_service_client:
            raise HTTPException(500, "Azure Storage not configured")
        
        blob_client = blob_service_client.get_blob_client(
            container=config.CONTAINER_NAME, blob=file.filename
        )
        blob_client.upload_blob(file.file, overwrite=True)
        return file.filename

    else:
        # --- LOCAL LOGIC ---
        file_location = f"{config.UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file.filename

def get_video_url(filename: str):
    """Returns the correct playback URL (Local Stream or Azure SAS)."""
    
    if config.STORAGE_MODE == "azure":
        # --- RETURN AZURE SAS URL ---
        if not blob_service_client:
             raise HTTPException(500, "Azure Storage not configured")
             
        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=config.CONTAINER_NAME,
            blob_name=filename,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        return f"https://{blob_service_client.account_name}.blob.core.windows.net/{config.CONTAINER_NAME}/{filename}?{sas_token}"

    else:
        # --- RETURN LOCAL STREAMING ENDPOINT ---
        # This points to the specialized streaming endpoint we created in Step 5
        return f"{config.BASE_URL}/stream/{filename}"
    
def list_videos():
    """Returns a list of all video filenames from Local or Azure."""
    
    if config.STORAGE_MODE == "azure":
        # --- AZURE LOGIC ---
        if not blob_service_client:
            return []
        
        container_client = blob_service_client.get_container_client(config.CONTAINER_NAME)
        # List all blobs in the container
        blob_list = container_client.list_blobs()
        return [blob.name for blob in blob_list]

    else:
        # --- LOCAL LOGIC ---
        if not os.path.exists(config.UPLOAD_DIR):
            return []
            
        # List all files in 'static' folder
        files = os.listdir(config.UPLOAD_DIR)
        # Filter to ensure we only return video files (optional)
        return [f for f in files if f.endswith(('.mp4', '.mov', '.avi'))]