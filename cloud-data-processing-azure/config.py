"""
config.py
---------
Loads Azure configuration from environment variables (via a local .env file).
Keeping credentials out of source code is a basic but important security practice.
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file in the project root (if present)
load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
RAW_CONTAINER_NAME = os.getenv("RAW_CONTAINER_NAME", "raw-data")
PROCESSED_CONTAINER_NAME = os.getenv("PROCESSED_CONTAINER_NAME", "processed-data")


def validate_config():
    """Raise a clear error early if required config is missing."""
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING is not set. "
            "Copy .env.example to .env and fill in your Azure Storage connection string."
        )
