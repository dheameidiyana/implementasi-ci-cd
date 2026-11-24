import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)


def upload_file(local_path: str | Path, blob_name: str) -> str:
    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient

    account = os.environ["AZURE_STORAGE_ACCOUNT"]
    container = os.getenv("AZURE_STORAGE_CONTAINER", "scraping-results")
    account_url = f"https://{account}.blob.core.windows.net"

    service = BlobServiceClient(
        account_url=account_url, credential=DefaultAzureCredential()
    )
    blob = service.get_blob_client(container=container, blob=blob_name)
    with open(local_path, "rb") as fh:
        blob.upload_blob(fh, overwrite=True)

    log.info("Uploaded %s -> %s/%s", local_path, container, blob_name)
    return blob.url