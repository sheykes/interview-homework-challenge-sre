#!/usr/bin/env python3
"""
myscript.py - System information utility
"""

import argparse
import psutil
import shutil


def bytes_to_human(n):
    for unit in ("B", "kB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def check_disk():
    print("=== Disk Stats ===")
    partitions = psutil.disk_partitions()
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        print(
            f"  Volume     : {part.device} ({part.mountpoint})\n"
            f"  Filesystem : {part.fstype}\n"
            f"  Total      : {bytes_to_human(usage.total)}\n"
            f"  Used       : {bytes_to_human(usage.used)}\n"
            f"  Free       : {bytes_to_human(usage.free)}\n"
            f"  Used %     : {usage.percent}%\n"
        )


def check_cpu():
    print("=== CPU Stats ===")
    freq = psutil.cpu_freq()
    print(
        f"  Cores (physical) : {psutil.cpu_count(logical=False)}\n"
        f"  Cores (logical)  : {psutil.cpu_count(logical=True)}\n"
        f"  Usage            : {psutil.cpu_percent(interval=1)}%\n"
        f"  Frequency (cur)  : {freq.current:.0f} MHz\n"
        f"  Frequency (min)  : {freq.min:.0f} MHz\n"
        f"  Frequency (max)  : {freq.max:.0f} MHz\n"
    )


def check_ram():
    print("=== RAM Stats ===")
    vm = psutil.virtual_memory()
    print(
        f"  Total  : {bytes_to_human(vm.total)}\n"
        f"  Used   : {bytes_to_human(vm.used)}\n"
        f"  Free   : {bytes_to_human(vm.available)}\n"
        f"  Used % : {vm.percent}%\n"
    )


def check_ports():
    print("=== Listening Ports ===")
    connections = psutil.net_connections(kind="inet")
    seen = set()
    rows = []
    for conn in connections:
        if conn.status == psutil.CONN_LISTEN:
            key = (conn.laddr.ip, conn.laddr.port, conn.type)
            if key in seen:
                continue
            seen.add(key)
            proto = "TCP" if conn.type == 1 else "UDP"
            pid = conn.pid or "-"
            try:
                name = psutil.Process(conn.pid).name() if conn.pid else "-"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                name = "-"
            rows.append((proto, conn.laddr.ip, conn.laddr.port, pid, name))

    if not rows:
        print("  No listening ports found (try running as root for full list).\n")
        return

    col_w = [6, 20, 7, 8, 20]
    header = f"  {'Proto':<{col_w[0]}}  {'Address':<{col_w[1]}}  {'Port':<{col_w[2]}}  {'PID':<{col_w[3]}}  {'Process'}"
    print(header)
    print("  " + "-" * (sum(col_w) + 8))
    for proto, ip, port, pid, name in sorted(rows, key=lambda x: x[2]):
        print(f"  {proto:<{col_w[0]}}  {ip:<{col_w[1]}}  {port:<{col_w[2]}}  {str(pid):<{col_w[3]}}  {name}")
    print()


def check_overview():
    print("=== Top 10 Processes by CPU Usage ===")
    procs = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    import time
    time.sleep(1)

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            info = proc.info
            procs.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top = sorted(procs, key=lambda p: p.get("cpu_percent") or 0, reverse=True)[:10]

    col_w = [7, 25, 8, 8, 12]
    header = (
        f"  {'PID':<{col_w[0]}}  {'Name':<{col_w[1]}}  "
        f"{'CPU %':<{col_w[2]}}  {'MEM %':<{col_w[3]}}  Status"
    )
    print(header)
    print("  " + "-" * (sum(col_w) + 8))
    for p in top:
        print(
            f"  {str(p['pid']):<{col_w[0]}}  "
            f"{(p['name'] or '-')[:25]:<{col_w[1]}}  "
            f"{(p['cpu_percent'] or 0):<{col_w[2]}.1f}  "
            f"{(p['memory_percent'] or 0):<{col_w[3]}.1f}  "
            f"{p.get('status', '-')}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="myscript.py",
        description="Myscript - a simple system information script",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )
    parser.add_argument("-d", "--disk",     action="store_true", help="check disk stats")
    parser.add_argument("-c", "--cpu",      action="store_true", help="check cpu stats")
    parser.add_argument("-p", "--ports",    action="store_true", help="check listen ports")
    parser.add_argument("-r", "--ram",      action="store_true", help="check ram stats")
    parser.add_argument("-o", "--overview", action="store_true", help="top 10 process with most CPU usage")
    parser.add_argument("-h", "--help",     action="store_true", help="show this help message and exit")

    args = parser.parse_args()

    if args.help or not any(vars(args).values()):
        print("Usage: myscript.py [options..]")
        print("Myscript - a simple system information script")
        print("")
        print("Myscript options:")
        print("  -d, --disk       check disk stats")
        print("  -c, --cpu        check cpu stats")
        print("  -p, --ports      check listen ports")
        print("  -r, --ram        check ram stats")
        print("  -o, --overview   top 10 process with most CPU usage.")
        print("  -h, --help       show this help message.")
        return

    if args.disk:
        check_disk()
    if args.cpu:
        check_cpu()
    if args.ram:
        check_ram()
    if args.ports:
        check_ports()
    if args.overview:
        check_overview()


if __name__ == "__main__":
    main()
