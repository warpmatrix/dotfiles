from scripts.utils.command_utils import (
    command_exists,
    execute_command,
)

is_initialized = False


def _initialize():
    global is_initialized
    if not is_initialized:
        update_package_manager()
        is_initialized = True


def update_package_manager():
    if command_exists("apt-get"):
        return execute_command("apt-get update", run_as_root=True)
    raise RuntimeError("Unsupported package manager. Only 'apt' is supported.")


def install_package(package: str):
    _initialize()
    if command_exists("apt-get"):
        return execute_command(f"apt-get install -y {package}", run_as_root=True)
    raise RuntimeError("Unsupported package manager. Only 'apt' is supported.")
