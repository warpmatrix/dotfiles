import argparse
import logging as logger
import pathlib
from typing import Callable, Dict

from scripts.utils.command_utils import (
    command_exists,
    execute_command,
)
from scripts.utils.operator_utils import download_file

logger.basicConfig(level=logger.INFO)

def install_go():
    # ref: https://golang.google.cn/doc/install
    url = "https://golang.google.cn/dl/go1.22.4.linux-amd64.tar.gz"
    output_path = "./downloads/go1.22.4.linux-amd64.tar.gz"

    download_file(url, output_path)
    execute_command("rm -rf /usr/local/go", run_as_root=True)
    execute_command(f"tar -C /usr/local -xzf {output_path}", run_as_root=True)


def install_nsys_cli():
    # ref: https://developer.nvidia.com/nsight-systems/get-started
    url = "https://developer.nvidia.com/downloads/assets/tools/secure/nsight-systems/2024_5/NsightSystems-linux-cli-public-2024.5.1.113-3461954.deb"
    output_path = "./downloads/NsightSystems-linux-cli-public-2024.5.1.113-3461954.deb"
    download_file(url, output_path)
    execute_command(f"apt install {output_path}", run_as_root=True)


def install_pyenv():
    # ref: https://github.com/pyenv/pyenv/
    assert command_exists("curl")
    execute_command("curl https://pyenv.run | bash")
    if command_exists("apt"):
        apt_plugin = "~/.dotfiles/dotbot-apt/apt.py"
        assert pathlib.Path(apt_plugin).expanduser().exists()
        config_path = "~/.dotfiles/configs/apt_pyenv_dep.conf.yaml"
        assert pathlib.Path(config_path).expanduser().exists()
        execute_command(f"~/.dotfiles/install -p {apt_plugin} -c {config_path}", run_as_root=True)


def install_fastfetch():
    arch = execute_command("arch").output
    if arch == "x86_64":
        arch = "amd64"
    url = f"https://github.com/fastfetch-cli/fastfetch/releases/download/2.47.0/fastfetch-linux-{arch}.deb"
    output_path = f"./downloads/fastfetch-linux-{arch}.deb"
    download_file(url, output_path)
    execute_command(f"apt install {output_path}", run_as_root=True)


def parse_args():
    parser = argparse.ArgumentParser()
    cmds = list(install.keys())
    parser.add_argument("command", type=str, help=f"the required command, choice: {cmds}")
    parser.add_argument("--force", "-f", action="store_true")
    args = parser.parse_args()
    return args


# using typing for better compatibility
install: Dict[str, Callable] = {
    "go": install_go,
    "nsys": install_nsys_cli,
    "pyenv": install_pyenv,
    "fastfetch": install_fastfetch,
}


if __name__ == "__main__":
    args = parse_args()
    if not command_exists(args.command) or args.force:
        install[args.command]()
