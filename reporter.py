import csv
import platform
from datetime import datetime
from pathlib import Path


def save_report(cpu_usage, ram_usage, disk_usage):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_dict = {
        "timestamp": timestamp,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage,
    }

    fieldnames = ["timestamp", "cpu_usage", "ram_usage", "disk_usage"]
    operating_system = platform.system()

    # C:\Users\USER\Upskill\windows-linux-server-monitor\
    folder_path = Path(__file__).resolve().parent
    log_dir = folder_path / "reports"
    log_dir.mkdir(parents=True, exist_ok=True)

    if operating_system == "Windows":
        folder_name = log_dir / "windows"
        folder_name.mkdir(parents=True, exist_ok=True)

    else:
        folder_name = log_dir / "linux"
        folder_name.mkdir(parents=True, exist_ok=True)

    csv_file = folder_name / "data.csv"
    if csv_file.is_file():
        print("The CSV file exists!")
        with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(my_dict)

    else:
        print("Creating the CSV file.")
        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(my_dict)
