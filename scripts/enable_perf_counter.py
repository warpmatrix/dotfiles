from pathlib import Path
from utils import *


def enable_perf_counter():
    conf_path = "/etc/modprobe.d/perf-counter.conf"
    f = Path(conf_path)
    if not f.exists():
        execute_command(f"touch {conf_path}", run_as_root=True)

    enable_str = "options nvidia NVreg_RestrictProfilingToAdminUsers=0"
    if not enable_str in f.read_text():
        execute_command(
            f"tee -a {conf_path}",
            input=enable_str,
            text=True,
            run_as_root=True,
        )
    assert enable_str in f.read_text()


def enable_perf_event():
    perf_event_paranoid = int(get_output("cat /proc/sys/kernel/perf_event_paranoid"))
    if perf_event_paranoid > 2:
        execute_command(
            f"tee -a /proc/sys/kernel/perf_event_paranoid",
            input=str(1),
            text=True,
            run_as_root=True,
        )

    conf_path = "/etc/sysctl.d/local.conf"
    f = Path(conf_path)
    if not f.exists():
        execute_command(f"touch {conf_path}", run_as_root=True)
    enable_str = "kernel.perf_event_paranoid=1"
    if not enable_str in f.read_text():
        execute_command(
            f"tee -a {conf_path}",
            input=enable_str,
            text=True,
            run_as_root=True,
        )
    assert enable_str in f.read_text()

if __name__ == "__main__":
    enable_perf_counter()
    enable_perf_event()
