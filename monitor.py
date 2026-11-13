import config
from logger import logger
import time
import platform
import psutil
from reporter import save_report


def get_cpu_usage():
    return psutil.cpu_percent(1)


def get_cpu_cores():
    phy_cores = psutil.cpu_count(logical=False)  # Physical cores
    log_cores = psutil.cpu_count(logical=True)  # Logical cores
    return phy_cores, log_cores


def check_cpu_alert(cpu_usage):
    logger.info(f"CPU Usage: {cpu_usage}%")

    if cpu_usage >= config.CPU_THRESHOLD:
        message = "WARNING: CPU usage is above the threshold!"
        logger.warning(message)
        return message
    message = "CPU usage is in normal condition."
    logger.info(message)
    return message


def get_ram_usage():
    ram_tuple = psutil.virtual_memory()

    total_bytes = ram_tuple.total
    total_GB = f"{total_bytes / (1024**3):.2f}"

    used_bytes = ram_tuple.used
    used_GB = f"{used_bytes / (1024**3):.2f}"

    available_bytes = ram_tuple.available
    available_GB = f"{available_bytes / (1024**3):.2f}"

    percent = ram_tuple.percent

    return total_GB, used_GB, available_GB, percent


def check_ram_alert(ram_usage):
    logger.info(f"RAM Usage: {ram_usage}%")

    if ram_usage >= config.RAM_THRESHOLD:
        message = "WARNING: RAM usage is above the threshold!"
        logger.warning(message)
        return message
    message = "RAM usage is in normal condition."
    logger.info(message)
    return message


def get_disk_usage():
    if platform.system() == "Windows":
        disk_path = "C:\\"
    else:
        disk_path = "/"

    disk_tuple = psutil.disk_usage(disk_path)

    total_disk_bytes = disk_tuple.total
    total_disk_GB = f"{total_disk_bytes / (1024**3):.2f}"

    used_disk_bytes = disk_tuple.used
    used_disk_GB = f"{used_disk_bytes / (1024**3):.2f}"

    free_disk_bytes = disk_tuple.free
    free_disk_GB = f"{free_disk_bytes / (1024**3):.2f}"

    percentage_disk = disk_tuple.percent

    return total_disk_GB, used_disk_GB, free_disk_GB, percentage_disk


def check_disk_alert(disk_usage):
    logger.info(f"Disk Usage: {disk_usage}%")

    if disk_usage >= config.DISK_THRESHOLD:
        message = "Disk usage is above the threshold!"
        logger.warning(message)
        return message

    message = "Disk usage is in normal condition."
    logger.info(message)
    return message


def get_top_processes():
    process_list = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] != "System Idle Process":
                proc.cpu_percent()
                process_list.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    time.sleep(1)

    processes = []
    for proc in process_list:
        try:
            processes.append(
                {
                    "pid": proc.info["pid"],
                    "name": proc.info["name"],
                    "cpu_percent": proc.cpu_percent(),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    sorted_processes = sorted(
        processes, key=lambda item: item["cpu_percent"], reverse=True
    )
    top_processes = sorted_processes[:5]
    return top_processes


def main():
    cpu_usage = get_cpu_usage()
    print(f"CPU Usage: {cpu_usage}%")
    cpu_alert = check_cpu_alert(cpu_usage)
    print(cpu_alert)

    phy_cores, log_cores = get_cpu_cores()
    print(f"Number of physical cpu cores: {phy_cores}")
    print(f"Number of logical cpu cores: {log_cores}")

    total_ram, used_ram, available_ram, percentage_ram = get_ram_usage()
    print(f"Total ram: {total_ram} GB")
    print(f"Used ram: {used_ram} GB")
    print(f"Available ram: {available_ram} GB")
    print(f"Used percentage of ram: {percentage_ram} %")
    print(check_ram_alert(percentage_ram))

    total_disk, used_disk, free_disk, percentage_disk = get_disk_usage()
    print(f"Total disk space: {total_disk} GB")
    print(f"Used disk space: {used_disk} GB")
    print(f"Free disk space: {free_disk} GB")
    print(f"Used percentage of disk: {percentage_disk} %")
    print(check_disk_alert(percentage_disk))

    print("Top 5 CPU-Consuming Processes")
    print(f"{'PID':<10}{'PROCESS NAME':<30}{'CPU %':>10}")

    for process in get_top_processes():
        pid = process["pid"]
        name = process["name"]
        cpu_percent = process["cpu_percent"]
        print(f"{pid:<10}{name:<30}{cpu_percent:>10.1f}")

    save_report(cpu_usage, percentage_ram, percentage_disk)


if __name__ == "__main__":
    main()
