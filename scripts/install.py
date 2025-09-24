import argparse
import logging as logger
import pathlib
from typing import Callable, Dict

from scripts.utils.command_utils import (
    command_exists,
    execute_command,
)
from scripts.utils.package_utils import (
    install_package,
    update_package_manager,
)
from scripts.utils.operator_utils import download_file
from scripts.utils.os_utils import (
    get_distribution,
    get_version,
    get_architecture,
)

logger.basicConfig(level=logger.INFO)


def install_cuda(cuda_version: str = "12-9"):
    distribution = get_distribution()
    assert distribution == "ubuntu"
    version = get_version()
    arch = get_architecture()
    url = f"https://developer.download.nvidia.com/compute/cuda/repos/{distribution}{version}/{arch}/cuda-keyring_1.1-1_all.deb"
    output_path = "./downloads/cuda-keyring_1.1-1_all.deb"
    download_file(url, output_path)
    execute_command(f"dpkg -i {output_path}", run_as_root=True)
    update_package_manager()
    if not command_exists("nvidia-smi"):
        install_package("nvidia-open")
    assert command_exists("nvidia-smi"), "nvidia-smi not found"
    install_package(f"cuda-toolkit-{cuda_version}")


def install_go():
    # ref: https://golang.google.cn/doc/install
    url = "https://golang.google.cn/dl/go1.22.4.linux-amd64.tar.gz"
    output_path = "./downloads/go1.22.4.linux-amd64.tar.gz"

    download_file(url, output_path)
    execute_command("rm -rf /usr/local/go", run_as_root=True)
    execute_command(f"tar -C /usr/local -xzf {output_path}", run_as_root=True)


def install_nsys_cli():
    # ref: https://developer.nvidia.com/nsight-systems/get-started
    url = "https://developer.nvidia.com/downloads/assets/tools/secure/nsight-systems/2025_5/NsightSystems-linux-cli-public-2025.5.1.121-3638078.deb"
    output_path = download_file(url)
    if command_exists("apt"):
        install_package(output_path)


def install_pyenv():
    # ref: https://github.com/pyenv/pyenv/
    assert command_exists("curl")
    execute_command("curl https://pyenv.run | bash")
    if command_exists("apt"):
        apt_plugin = "~/.dotfiles/dotbot-apt/apt.py"
        assert pathlib.Path(apt_plugin).expanduser().exists()
        config_path = "~/.dotfiles/configs/apt_pyenv_dep.conf.yaml"
        assert pathlib.Path(config_path).expanduser().exists()
        execute_command(
            f"~/.dotfiles/install -p {apt_plugin} -c {config_path}", run_as_root=True
        )


def install_fastfetch():
    arch = get_architecture()
    if arch == "x86_64":
        arch = "amd64"
    url = f"https://github.com/fastfetch-cli/fastfetch/releases/download/2.47.0/fastfetch-linux-{arch}.deb"
    output_path = f"./downloads/fastfetch-linux-{arch}.deb"
    download_file(url, output_path)
    install_package(output_path)


def parse_args():
    parser = argparse.ArgumentParser()
    cmds = list(install.keys())
    parser.add_argument(
        "command", type=str, help=f"the required command, choice: {cmds}"
    )
    parser.add_argument("--force", "-f", action="store_true")
    args = parser.parse_args()
    return args


# using typing for better compatibility
install: Dict[str, Callable] = {
    "cuda": install_cuda,
    "fastfetch": install_fastfetch,
    "go": install_go,
    "nsys": install_nsys_cli,
    "pyenv": install_pyenv,
}


if __name__ == "__main__":
    args = parse_args()
    if not command_exists(args.command) or args.force:
        install[args.command]()
