import argparse
from typing import Callable

from utils import *


def install_go():
    # ref: https://golang.google.cn/doc/install
    url = "https://golang.google.cn/dl/go1.22.4.linux-amd64.tar.gz"
    output_path = "downloads/go1.22.4.linux-amd64.tar.gz"

    download_file(url, output_path)
    execute_command("rm -rf /usr/local/go", run_as_root=True)
    execute_command(f"tar -C /usr/local -xzf {output_path}", run_as_root=True)


def install_nsys_cli():
    # ref: https://developer.nvidia.com/nsight-systems/get-started
    url = "https://developer.nvidia.com/downloads/assets/tools/secure/nsight-systems/2024_5/NsightSystems-linux-cli-public-2024.5.1.113-3461954.deb"
    output_path = "./downloads/NsightSystems-linux-cli-public-2024.5.1.113-3461954.deb"
    download_file(url, output_path)
    execute_command(f"apt install {output_path}", run_as_root=True)


def parse_args():
    parser = argparse.ArgumentParser()
    cmds = list(install.keys())
    parser.add_argument("command", type=str, help=f"the required command, choice: {cmds}")
    parser.add_argument("--force", "-f", action="store_true")
    args = parser.parse_args()
    return args


install: dict[str, Callable] = {
    "go": install_go,
    "nsys": install_nsys_cli,
}


if __name__ == "__main__":
    args = parse_args()
    if not command_exists(args.command) or args.force:
        install[args.command]()
