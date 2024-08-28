import os
import urllib.request
import shutil
import subprocess
import sys

from loguru import logger
from pathlib import Path


def download_file(url, output_path: str, force: bool = False):
    file_path = Path(output_path)
    if file_path.exists() and not force:
        logger.info(f"File {file_path} exists")
        return

    try:
        os.makedirs(file_path.parent, exist_ok=True)
        urllib.request.urlretrieve(url, file_path)
        logger.info(f"File downloaded successfully to {output_path}")
    except Exception as e:
        logger.error(f"Failed to download file: {e}")
        sys.exit(1)


def is_root_user():
    return os.geteuid() == 0


def get_output(command: str, run_as_root: bool = False):
    if run_as_root and not is_root_user():
        assert command_exists("sudo")
        command = "sudo " + command

    try:
        logger.debug(f"get output: {command}")
        return subprocess.getoutput(command)
    except Exception as e:
        print(f"Failed to execute command: {command}, {e}")
        sys.exit(1)


def execute_command(command: str, run_as_root: bool = False, input=None, text=None):
    args = command.split(" ")
    if run_as_root and not is_root_user():
        assert command_exists("sudo")
        command = "sudo " + command

    try:
        logger.info(f"executing command: {command}")
        subprocess.run(command, shell=True)
        command = " ".join(args)
    except Exception as e:
        print(f"Failed to execute command: {command}, {e}")
        sys.exit(1)


def command_exists(command: str):
    return shutil.which(command) is not None
