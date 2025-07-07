import logging as logger
import os
import sys

from pathlib import Path
from urllib import request


def download_file(url: str, output_path: str, force: bool = False):
    file_path = Path(output_path)
    if file_path.exists() and not force:
        logger.info(f"File {file_path} exists")
        return

    try:
        os.makedirs(file_path.parent, exist_ok=True)
        request.urlretrieve(url, file_path)
        logger.info(f"File downloaded successfully to {output_path}")
    except Exception as e:
        logger.error(f"Failed to download file: {e}")
        sys.exit(1)

