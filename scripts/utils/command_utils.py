import enum
import logging as logger
import os
import shutil
import subprocess
import sys

from typing import (
    NamedTuple,
    Optional,
)


class CommandOutput(NamedTuple):
    exit_code: int
    output: str


class CommandFile(enum.auto):
    PIPE = subprocess.PIPE


def is_root_user():
    return os.geteuid() == 0


def to_sudo_command(command: str):
    assert command_exists("sudo")
    args = ["sudo"] + command.split()
    command = " ".join(args)
    return command


def execute_command(command: str, run_as_root: bool = False):
    # support redirect using '>' or '<'
    if run_as_root and not is_root_user():
        command = to_sudo_command(command)

    try:
        logger.debug(f"executing command: {command}")
        status_output = subprocess.getstatusoutput(command)
        return CommandOutput(*status_output)
    except Exception as e:
        print(f"Failed to execute command: {command}, {e}")
        sys.exit(1)


def create_process(
    command: str,
    run_as_root: bool = False,
    stdin: Optional[CommandFile] = None,
    stdout: Optional[CommandFile] = None,
    stderr: Optional[CommandFile] = None,
):
    if run_as_root and not is_root_user():
        command = to_sudo_command(command)

    logger.debug(f"create process with command: {command}")
    args = command.split()
    cmd = subprocess.Popen(args, stdin=stdin, stdout=stdout, stderr=stderr)
    return cmd


def command_exists(command: str):
    return shutil.which(command) is not None
