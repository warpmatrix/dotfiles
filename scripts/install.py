import argparse
from typing import Callable

from utils import *

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
