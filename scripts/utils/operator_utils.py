import logging as logger
import os
import sys

from typing import Optional
from pathlib import Path
from urllib import request

DOWNLOAD_DIR="./downloads"

def download_file(url: str, output_path: Optional[str] = None, force: bool = False):
    if output_path is None:
        output_path = f"{DOWNLOAD_DIR}/{Path(url).name}"
    file_path = Path(output_path)
    if file_path.exists() and not force:
        logger.info(f"File {file_path} exists")
        return output_path

    try:
        os.makedirs(file_path.parent, exist_ok=True)
        request.urlretrieve(url, file_path)
        logger.info(f"File downloaded successfully to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to download file: {e}")
        sys.exit(1)

