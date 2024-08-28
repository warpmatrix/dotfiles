import pathlib
from utils import *


# TODO: refact using abstract factory
def enable_docker_cmpl():
    path = pathlib.Path("~/.config/fish/completions/docker.fish").expanduser()
    if path.exists():
        return
    execute_command("docker completion fish > ~/.config/fish/completions/docker.fish")


if __name__ == "__main__":
    if command_exists("docker"):
        enable_docker_cmpl()
