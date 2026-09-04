"""
main.py
-------
Entry point for the pipeline:

  1. Upload a local raw data file to Azure Blob Storage (raw container)
  2. Download it back from Azure (simulating a processing worker)
  3. Process/clean the data locally
  4. Upload the processed result to Azure Blob Storage (processed container)
  5. Confirm by listing blobs in both containers

Run with:  python main.py
"""

import os
from blob_helper import BlobHelper
from data_processor import process_csv
import config

LOCAL_INPUT_FILE = "sample_data/sample.csv"
LOCAL_DOWNLOADED_FILE = "workspace/downloaded_sample.csv"
LOCAL_PROCESSED_FILE = "workspace/processed_sample.csv"


def main():
    print("=== Cloud Data Processing Using Azure ===\n")

    blob = BlobHelper()

    # Step 1: Upload raw file
    print("Step 1: Uploading raw data to Azure...")
    blob_name = blob.upload_file(config.RAW_CONTAINER_NAME, LOCAL_INPUT_FILE)

    # Step 2: Download it back down (this is where a real pipeline would
    # typically run inside an Azure Function or a separate processing job)
    print("\nStep 2: Downloading raw data from Azure...")
    blob.download_file(config.RAW_CONTAINER_NAME, blob_name, LOCAL_DOWNLOADED_FILE)

    # Step 3: Process the data
    print("\nStep 3: Processing data...")
    process_csv(LOCAL_DOWNLOADED_FILE, LOCAL_PROCESSED_FILE)

    # Step 4: Upload processed data
    print("\nStep 4: Uploading processed data to Azure...")
    blob.upload_file(config.PROCESSED_CONTAINER_NAME, LOCAL_PROCESSED_FILE)

    # Step 5: Confirm
    print("\nStep 5: Current contents of each container:")
    print(f"  {config.RAW_CONTAINER_NAME}: {blob.list_blobs(config.RAW_CONTAINER_NAME)}")
    print(f"  {config.PROCESSED_CONTAINER_NAME}: {blob.list_blobs(config.PROCESSED_CONTAINER_NAME)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
