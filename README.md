# Windows & Linux Server Monitor

A cross-platform system monitoring tool built with Python and `psutil`. It collects system resource information, identifies resource-intensive processes, checks configurable thresholds, and records monitoring data on Windows and Linux environments.

## Features

- CPU utilization monitoring
- Physical and logical CPU core information
- RAM usage monitoring
- Disk space monitoring
- Top 5 CPU-consuming processes
- Configurable CPU, RAM, and disk thresholds
- Resource status checks and warning logs
- Timestamped monitoring logs
- CSV reports for historical monitoring data
- Bash script for Linux execution
- Automated monitoring using Windows Task Scheduler and Linux cron
- Resource simulation for testing monitoring behavior
- Automated unit testing with pytest

## Technologies

- Python
- psutil
- pytest
- Bash
- Git and GitHub
- Windows Task Scheduler
- Linux cron
- CSV

## Supported Operating Systems

- Windows
- Ubuntu 26.04.1 LTS (tested through WSL2)

**Note:** Linux testing was performed using Ubuntu under Windows Subsystem for Linux 2 (WSL2), not a dedicated Ubuntu Server installation.

## Project Structure

```text
windows-linux-server-monitor/
│
├── logs/
│   ├── windows/
│   │   └── monitor.log
│   └── linux/
│       └── monitor.log
│
├── reports/
│   ├── windows/
│   │   └── data.csv
│   └── linux/
│       └── data.csv
│
├── scripts/
│   └── run_monitor.sh
│
├── tests/
│   ├── test_monitor.py
│   └── test_reporter.py
│
├── .gitignore
├── config.py
├── logger.py
├── monitor.py
├── reporter.py
├── requirements.txt
├── simulator.py
└── README.md
```

## Prerequisites

- Python 3.10 or later
- Git
- Windows or Ubuntu Linux
- WSL2 with Ubuntu for Linux testing on Windows

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/JayceeMolina/windows-linux-server-monitor.git
cd windows-linux-server-monitor
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

**Ubuntu/Linux:**

```bash
python3 -m venv .venv-linux
```

Activate it:

```bash
source .venv-linux/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Thresholds

Edit `config.py` to adjust the resource warning thresholds.

```python
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
DISK_THRESHOLD = 90
```

### 5. Run the Monitor

**Windows:**

```powershell
python monitor.py
```

**Ubuntu/Linux:**

```bash
python3 monitor.py
```

## Automated Testing

The project uses pytest to run automated unit tests for monitoring alerts and CSV reporting.

Current test coverage includes:

- CPU, RAM, and disk threshold checks.
- CSV report creation and header validation.
- CSV data accuracy.
- Appending new records without duplicating CSV headers.

Run the tests from the project root:

```bash
python -m pytest -v
```

The `-v` option displays individual test names and their results.

## Linux Setup (Ubuntu through WSL2)

Install WSL2 and Ubuntu, then open the Ubuntu terminal.

Navigate to the project directory. If the repository is stored on the Windows filesystem:

```bash
cd /mnt/c/Users/USER/Upskill/windows-linux-server-monitor
```

Create and activate the Linux virtual environment:

```bash
python3 -m venv .venv-linux
source .venv-linux/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the monitoring script:

```bash
python3 monitor.py
```

## Bash Automation

The project includes `scripts/run_monitor.sh` to simplify running the monitoring tool on Linux.

First, give the script execution permission:

```bash
chmod +x scripts/run_monitor.sh
```

Run it using:

```bash
./scripts/run_monitor.sh
```

The script:

- Navigates to the project root directory.
- Detects an available Python interpreter.
- Prioritizes the active virtual environment when available.
- Uses the project's Linux virtual environment when available.
- Falls back to an available Python installation.
- Executes `monitor.py`.

## Scheduled Monitoring

The monitoring tool supports automated execution every five minutes using Windows Task Scheduler and Linux cron.

### Windows Task Scheduler

Create a scheduled task using PowerShell:

```powershell
schtasks /Create /SC MINUTE /MO 5 /TN "WindowsLinuxServerMonitor" /TR "C:\path\to\project\.venv\Scripts\pythonw.exe C:\path\to\project\monitor.py" /F
```

Replace the example paths with the actual project paths on your computer.

`pythonw.exe` runs the monitoring script without opening a console window.

To check the scheduled task:

```powershell
schtasks /Query /TN "WindowsLinuxServerMonitor"
```

To disable it:

```powershell
schtasks /Change /TN "WindowsLinuxServerMonitor" /DISABLE
```

To enable it again:

```powershell
schtasks /Change /TN "WindowsLinuxServerMonitor" /ENABLE
```

### Linux Cron

Start the cron service:

```bash
sudo service cron start
```

Open the crontab editor:

```bash
crontab -e
```

Add the following entry to execute the monitoring script every five minutes:

```cron
*/5 * * * * /bin/bash /mnt/c/Users/USER/Upskill/windows-linux-server-monitor/scripts/run_monitor.sh
```

Replace the path with the actual location of the project.

Check the scheduled entries:

```bash
crontab -l
```

Check the cron service:

```bash
sudo service cron status
```

Stop the cron service:

```bash
sudo service cron stop
```

**Note:** Windows Task Scheduler requires Windows to be running. Linux cron under WSL2 requires the WSL environment to be running.

## Resource Simulation

The project includes `simulator.py` to generate temporary system resource usage for testing.

The simulator:

- Generates CPU load using a separate process.
- Allocates 256 MB of RAM.
- Creates a temporary 100 MB disk file.
- Runs the simulation for 30 seconds.
- Terminates the CPU process, releases allocated memory, and removes the temporary file after execution.

Run the simulator:

```bash
python simulator.py
```

While the simulator is running, execute `monitor.py` separately to observe the resource usage.

### Windows Simulation Test Results

The following results were collected during testing on Windows.

| Metric | Before Simulation | During Simulation |
|---|---:|---:|
| CPU utilization | 12.1% | 14.0% |
| RAM utilization | 64.9% | 65.9% |
| Disk utilization | 95.8% | 95.8% |
| Disk free space | 19.99 GB | 19.89 GB |

**Additional observations:**

- The simulator's Python process appeared in the top CPU-consuming processes with 100% process CPU utilization.
- RAM utilization increased by approximately 1 percentage point.
- Disk free space decreased by approximately 100 MB.
- The disk threshold warning was recorded in the monitoring log.
- CPU and RAM remained below their configured warning thresholds during this test.
- Temporary resources were cleaned up after the simulation.

**Note:** The 100% CPU utilization shown for the simulator process represents that individual process, not the overall CPU utilization of the machine. The overall CPU reading is averaged across the system's logical processors.

The disk was already above its configured 90% threshold before the simulation began, so the disk warning was not caused by the simulator.

The simulator was tested on Windows. Linux simulator testing was not performed.

## Logging and Reporting

The project maintains separate monitoring logs and CSV reports for each operating system.

**Windows output:**

```text
logs/windows/monitor.log
reports/windows/data.csv
```

**Linux output:**

```text
logs/linux/monitor.log
reports/linux/data.csv
```

The monitoring log records resource status and threshold warnings with timestamps.

The CSV report stores timestamped CPU, RAM, and disk utilization readings for later inspection.

## Development Setup

To set up the project from scratch:

1. Create the project directory.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Create the configuration, monitoring, logging, and reporting modules.
5. Implement the Bash execution script.
6. Configure the appropriate output directories.
7. Test the monitoring tool on Windows and Ubuntu.
8. Configure automated execution using Task Scheduler and cron.
9. Write and execute automated unit tests using pytest.

## Git Workflow

Initialize the repository:

```bash
git init
```

Stage project files:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Initial project setup"
```

Push the project to GitHub:

```bash
git push -u origin main
```

For future development, create a separate branch:

```bash
git checkout -b feature/your-feature
```

Commit and push changes on that branch, then open a Pull Request to merge them into `main`.

## CI/CD

- GitHub Actions automatically runs the project's automated tests on every push and pull request targeting the main branch.
- The workflow uses Ubuntu and Windows runners to execute the pytest test suite.
- During CI testing, a cross-platform path issue was discovered: The report tests expected the Windows directory even when running on Linux. This was fixed by making the expected report directory depend on the operating system.

## Future Improvements

- Email or external notification integration for threshold warnings.
- JSON reporting support.
- Automated integration testing.
- Additional monitoring metrics.
- Improved resource simulation and testing scenarios.
- Multi-device monitoring to collect and monitor resource metrics from multiple machines simultaneously.

## Limitations

- Monitoring results depend on the operating system and environment where the tool is executed.
- Automated execution under WSL2 depends on the WSL environment remaining active.
- The simulator generates temporary resource usage for testing and does not represent actual production workloads.