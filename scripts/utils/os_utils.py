import distro
import platform


def get_distribution():
    return distro.id()


def get_version():
    return "".join(distro.version().split("."))


def get_architecture():
    return platform.machine()
