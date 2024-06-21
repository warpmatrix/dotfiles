import argparse
import os
import urllib.request
import shutil
import subprocess
import sys

from loguru import logger
from pathlib import Path
from typing import Callable

def download_file(url, output_path_str: str, replace: bool = False):
    output_path = Path(output_path_str)
    if output_path.exists() and not replace:
        logger.info(f"File {output_path} exists")
        return
    
    try:
        os.makedirs(output_path.parent, exist_ok=True)
        urllib.request.urlretrieve(url, output_path)
        logger.info(f"File downloaded successfully to {output_path_str}")
    except Exception as e:
        logger.error(f"Failed to download file: {e}")
        sys.exit(1)


def is_root_user():
    return os.geteuid() == 0


def execute_command(command: str, run_as_root: bool = False):
    args = command.split(" ")
    if run_as_root and not is_root_user():
        assert command_exists("sudo")
        args = ["sudo"] + args

    try:
        subprocess.run(args)
        command = " ".join(args)
        logger.info(f"Command executed: {command}")
    except Exception as e:
        print(f"Failed to execute command: {e}")
        sys.exit(1)


def command_exists(command: str):
    return shutil.which(command) is not None


def install_go():
    # ref: https://golang.google.cn/doc/install
    url = "https://golang.google.cn/dl/go1.22.4.linux-amd64.tar.gz"
    output_path = "downloads/go1.22.4.linux-amd64.tar.gz"

    download_file(url, output_path)
    execute_command("rm -rf /usr/local/go", run_as_root=True)
    execute_command("tar -C /usr/local -xzf downloads/go1.22.4.linux-amd64.tar.gz", run_as_root=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", "-c", type=str)
    args = parser.parse_args()
    return args


install: dict[str, Callable] = {
    "go": install_go
}


if __name__ == "__main__":
    args = parse_args()
    if not command_exists(args.command):    
        install[args.command]()
