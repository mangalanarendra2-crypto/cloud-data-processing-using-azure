"""
blob_helper.py
--------------
Thin wrapper around the Azure Blob Storage SDK.
Handles: connecting to the storage account, creating containers if needed,
uploading local files, and downloading blobs to local disk.
"""

import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

import config


class BlobHelper:
    def __init__(self):
        config.validate_config()
        self.service_client = BlobServiceClient.from_connection_string(
            config.AZURE_STORAGE_CONNECTION_STRING
        )

    def ensure_container(self, container_name: str):
        """Create the container if it doesn't already exist."""
        try:
            self.service_client.create_container(container_name)
            print(f"Container '{container_name}' created.")
        except ResourceExistsError:
            # Container already exists — nothing to do.
            pass

    def upload_file(self, container_name: str, local_path: str, blob_name: str = None):
        """Upload a local file to the given container."""
        self.ensure_container(container_name)
        blob_name = blob_name or os.path.basename(local_path)

        container_client = self.service_client.get_container_client(container_name)
        with open(local_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)

        print(f"Uploaded '{local_path}' -> container '{container_name}' as '{blob_name}'")
        return blob_name

    def download_file(self, container_name: str, blob_name: str, local_path: str):
        """Download a blob to a local file path."""
        container_client = self.service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)

        os.makedirs(os.path.dirname(local_path) or ".", exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(blob_client.download_blob().readall())

        print(f"Downloaded '{blob_name}' from container '{container_name}' -> '{local_path}'")
        return local_path

    def list_blobs(self, container_name: str):
        """List all blob names in a container."""
        self.ensure_container(container_name)
        container_client = self.service_client.get_container_client(container_name)
        return [b.name for b in container_client.list_blobs()]
