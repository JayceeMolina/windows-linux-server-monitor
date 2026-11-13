import logging
import os
import platform

operating_system = platform.system()
# C:\Users\USER\Upskill\windows-linux-server-monitor\logger.py
file_path = os.path.abspath(__file__)

# C:\Users\USER\Upskill\windows-linux-server-monitor
project_dir = os.path.dirname(file_path)
log_dir = os.path.join(project_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

if operating_system == "Windows":
    folder_name = os.path.join(log_dir, "windows")
    os.makedirs(folder_name, exist_ok=True)
    file_name = os.path.join(folder_name, "monitor.log")

else:
    folder_name = os.path.join(log_dir, "linux")
    os.makedirs(folder_name, exist_ok=True)
    file_name = os.path.join(folder_name, "monitor.log")


logging.basicConfig(
    filename=file_name,
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s: %(message)s",
)
logger = logging.getLogger("server_monitor")
