from pathlib import Path

from scripts.utils.command_utils import (
    command_exists,
    execute_command,
)


# TODO: refact using abstract factory
def enable_docker_cmpl():
    path = Path("~/.config/fish/completions/docker.fish").expanduser()
    if path.exists():
        return
    execute_command("docker completion fish > ~/.config/fish/completions/docker.fish")


if __name__ == "__main__":
    if command_exists("docker"):
        enable_docker_cmpl()
