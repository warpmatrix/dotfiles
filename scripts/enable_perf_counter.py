from pathlib import Path
from utils import *


def enable_perf_counter():
    conf_path = "/etc/modprobe.d/perf-counter.conf"
    f = Path(conf_path)
    if not f.exists():
        execute_command(f"touch {conf_path}", run_as_root=True)

    enable_str = "options nvidia NVreg_RestrictProfilingToAdminUsers=0"
    if not enable_str in f.read_text():
        proc = create_process(
            f"tee -a {conf_path}", run_as_root=True, stdin=CommandFile.PIPE
        )
        proc.communicate(enable_str.encode())
    assert enable_str in f.read_text()


def enable_perf_event():
    perf_event_paranoid = int(execute_command("cat /proc/sys/kernel/perf_event_paranoid").output)
    if perf_event_paranoid > 2:
        proc = create_process(
            f"tee -a /proc/sys/kernel/perf_event_paranoid",
            run_as_root=True,
            stdin=CommandFile.PIPE,
        )
        proc.communicate("1".encode())

    conf_path = "/etc/sysctl.d/local.conf"
    f = Path(conf_path)
    if not f.exists():
        execute_command(f"touch {conf_path}", run_as_root=True)
    enable_str = "kernel.perf_event_paranoid=1"
    if not enable_str in f.read_text():
        proc = create_process(
            f"tee -a {conf_path}", run_as_root=True, stdin=CommandFile.PIPE
        )
        proc.communicate(enable_str.encode())
    assert enable_str in f.read_text()


if __name__ == "__main__":
    enable_perf_counter()
    enable_perf_event()
