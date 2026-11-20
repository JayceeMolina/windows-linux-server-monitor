# Windows & Linux Server Monitor

A cross-platform system monitoring tool built with Python and [psutil](https://pypi.org/project/psutil/). It collects system resource information, identifies resource-intensive processes, checks configurable thresholds, and records monitoring data on Windows and Linux.

The project supports native execution, Docker, and Docker Compose, with automated testing and configurable Docker Hub publishing through GitHub Actions.

## Features

- **CPU monitoring** – Tracks CPU utilization and physical/logical core information.
- **Memory monitoring** – Tracks RAM utilization.
- **Disk monitoring** – Tracks disk space utilization.
- **Process monitoring** – Identifies the top 5 CPU-consuming processes.
- **Configurable thresholds** – Sets CPU, RAM, and disk warning thresholds.
- **Resource alerts** – Records resource status and threshold warnings.
- **Logging** – Generates timestamped monitoring logs.
- **CSV reporting** – Stores historical CPU, RAM, and disk readings.
- **Cross-platform execution** – Supports Windows and Linux.
- **Automated scheduling** – Supports Windows Task Scheduler and Linux cron.
- **Resource simulation** – Generates temporary CPU, memory, and disk activity for testing.
- **Docker support** – Builds and runs the application using Docker and Docker Compose.
- **Automated testing** – Uses pytest to validate monitoring and reporting functionality.
- **CI/CD pipeline** – Uses GitHub Actions to run cross-platform tests, validate Docker builds, and optionally publish images to Docker Hub.

## Technologies

- Python 3.11
- psutil
- pytest
- Bash
- Docker
- Docker Compose
- Docker Buildx
- Docker Hub
- Git and GitHub
- GitHub Actions
- Windows Task Scheduler
- Linux cron
- CSV

## Supported Environments

- Windows
- Ubuntu 26.04.1 LTS (tested through WSL2)
- Docker with Linux containers

**Testing notes:**

- Linux testing was performed using Ubuntu under Windows Subsystem for Linux 2 (WSL2), not a dedicated Ubuntu Server installation.
- Docker testing was performed using Docker Desktop with the WSL2 backend.

## Project Structure

```text
windows-linux-server-monitor/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── logs/
│   ├── windows/
│   └── linux/
│
├── reports/
│   ├── windows/
│   └── linux/
│
├── scripts/
│   └── run_monitor.sh
│
├── tests/
│   ├── test_monitor.py
│   └── test_reporter.py
│
├── .dockerignore
├── .gitignore
├── compose.yaml
├── Dockerfile
├── config.py
├── logger.py
├── monitor.py
├── reporter.py
├── requirements.txt
├── simulator.py
└── README.md
```

## Prerequisites

### Native execution

- Python 3.11
- Git
- Windows or Ubuntu Linux

For Linux testing on Windows, WSL2 with Ubuntu is recommended.

### Docker execution

- Docker Desktop or Docker Engine
- Docker Compose

For Windows users, Docker Desktop with WSL2 integration is recommended.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/JayceeMolina/windows-linux-server-monitor.git
cd windows-linux-server-monitor
```

### 2. Create a virtual environment

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure resource thresholds

Edit `config.py` to adjust the warning thresholds.

Default configuration:

```python
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
DISK_THRESHOLD = 90
```

### 5. Run the monitor

**Windows:**

```powershell
python monitor.py
```

**Ubuntu/Linux:**

```bash
python3 monitor.py
```

The application collects system resource information, checks configured thresholds, records monitoring logs, and appends a row to the CSV report before exiting.

## Automated Testing

The project uses pytest to run automated unit tests for monitoring and CSV reporting.

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
cd /mnt/c/Users/<your-windows-username>/path/to/windows-linux-server-monitor
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

Give the script execution permission:

```bash
chmod +x scripts/run_monitor.sh
```

Run it:

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

Check the scheduled task:

```powershell
schtasks /Query /TN "WindowsLinuxServerMonitor"
```

Disable the task:

```powershell
schtasks /Change /TN "WindowsLinuxServerMonitor" /DISABLE
```

Enable it again:

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

Add an entry to execute the monitoring script every five minutes:

```cron
*/5 * * * * /bin/bash /mnt/c/Users/<your-windows-username>/path/to/windows-linux-server-monitor/scripts/run_monitor.sh
```

Replace the path with the actual location of the project.

Check scheduled entries:

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

## Docker

The project includes a Dockerfile and Docker Compose configuration for building and running the application in a Linux container.

### Local Docker build

From the project root, build the image:

```bash
docker compose build
```

This reads `compose.yaml`, uses the current project directory as the build context, and builds the image using the project's Dockerfile.

Run the monitoring application:

```bash
docker compose run --rm monitor
```

The container executes `monitor.py` and exits after the monitoring process finishes.

The `--rm` option automatically removes the container after it exits.

### Persistent logs and reports

The Compose configuration uses bind mounts to preserve monitoring output on the host machine.

```yaml
services:
  monitor:
    build: .
    container_name: server-monitor
    volumes:
      - ./logs:/app/logs
      - ./reports:/app/reports
```

The bind mounts connect local project directories to directories inside the container.

| Host directory | Container directory |
|---|---|
| `./logs` | `/app/logs` |
| `./reports` | `/app/reports` |

Logs and CSV reports generated inside the container are accessible from the project directory on the host machine.

Docker execution creates the following output paths:

```text
logs/
└── linux/
    └── monitor.log

reports/
└── linux/
    └── data.csv
```

The output is stored under `linux` because the application runs inside a Linux container, even when Docker Desktop is running on Windows.

The bind mounts also allow the generated files to remain available after the container is removed.

### Run tests inside Docker

```bash
docker compose run --rm monitor python -m pytest -v
```

This overrides the Dockerfile's default startup command for that execution and runs the test suite instead.

### Docker configuration

**Dockerfile**

Defines how the application image is built. It uses `python:3.11-slim` as the base image, installs the required Python dependencies, copies the project files, and sets the default command to execute `monitor.py`.

**.dockerignore**

Excludes unnecessary files from the Docker build context, including:

- Python virtual environments.
- Python cache files.
- Git metadata.
- IDE settings.
- Existing logs and reports.
- Environment files.

These exclusions prevent unnecessary local files from being sent to Docker during the image build. They do not delete the files from the project or change Git tracking.

**compose.yaml**

Defines the monitoring service, image build configuration, container name, and bind mounts for persistent output.

### Docker monitoring limitation

The application monitors the environment visible to the container by default, not the entire host machine.

For example, when running a Linux container through Docker Desktop on Windows, the application sees a Linux container environment rather than the Windows host environment.

Docker Desktop uses its WSL2-based Linux environment to run Linux containers. Therefore, the application reports information from its container environment instead of native Windows host metrics.

Use native Windows or Linux execution when monitoring the respective host operating systems directly.

## Docker Hub

A prebuilt Docker image is available on Docker Hub:

**Image:** `jayceemolina/windows-linux-server-monitor:latest`

**Repository:** [Docker Hub – Windows & Linux Server Monitor](https://hub.docker.com/r/jayceemolina/windows-linux-server-monitor)

Using the published image allows users to run the application without cloning the source repository, installing Python dependencies, or building the image locally.

### 1. Pull the image

```bash
docker pull jayceemolina/windows-linux-server-monitor:latest
```

Because the repository is public, Docker Hub authentication is not normally required to pull the image.

### 2. Create output directories

**Ubuntu/Linux:**

```bash
mkdir -p logs reports
```

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Force logs, reports | Out-Null
```

### 3. Run the image

**Ubuntu/Linux:**

```bash
docker run --rm \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/reports:/app/reports" \
  jayceemolina/windows-linux-server-monitor:latest
```

**Windows PowerShell:**

```powershell
docker run --rm `
  -v "${PWD}/logs:/app/logs" `
  -v "${PWD}/reports:/app/reports" `
  jayceemolina/windows-linux-server-monitor:latest
```

The bind mounts make the container's logs and CSV reports accessible from the current host directory.

The container runs once and exits after monitoring. The `--rm` option removes the container automatically, while the mounted output files remain on the host.

**Note:** Pulling the published image does not require a Docker Hub account because the repository is public. Docker Desktop or Docker Engine must still be installed and running.

### Image tags

The project currently publishes the `latest` tag.

This tag points to the most recently published image. When a new image is pushed using the same tag, Docker Hub updates the tag to point to the newly published image.

To retrieve the latest published version:

```bash
docker pull jayceemolina/windows-linux-server-monitor:latest
```

## Automated Docker Hub Publishing with GitHub Actions

The project uses GitHub Actions to automate cross-platform testing, Docker image building, and optional Docker Hub publishing.

The workflow is located at:

```text
.github/workflows/tests.yml
```

### Workflow triggers

The workflow runs on:

- Pushes to `main`.
- Pull requests targeting `main`.

### 1. Cross-platform testing

The `test` job runs on:

- `ubuntu-latest`
- `windows-latest`

Each runner checks out the repository, sets up Python 3.11, installs dependencies, and runs:

```bash
python -m pytest -v
```

Both test jobs must pass before the Docker build job can proceed.

### 2. Docker build validation

The `docker-build` job depends on the successful completion of the `test` job.

It uses:

- An Ubuntu GitHub-hosted runner.
- Docker Buildx.
- Docker Build Push Action.

The job builds the Docker image to validate that the Docker configuration and application can be built successfully.

Docker image building also runs for pull requests, but the image is not published.

### 3. Configurable Docker Hub publishing

The workflow can automatically publish the Docker image to Docker Hub when changes reach `main`.

Publishing is controlled through GitHub repository variables.

**Repository variables**

| Variable | Purpose |
|---|---|
| `ENABLE_DOCKERHUB_PUBLISHING` | Enables or disables automatic publishing. |
| `DOCKERHUB_IMAGE` | Defines the Docker Hub image name and tag. |

The repository also uses these GitHub Actions secrets:

**Repository secrets**

| Secret | Purpose |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username. |
| `DOCKERHUB_TOKEN` | Docker Hub access token used for authentication. |

### Configure publishing for your own repository

If you fork or clone this project and want your own GitHub Actions workflow to publish Docker images, you must configure your own Docker Hub repository and GitHub Actions settings.

First, create a repository on Docker Hub for your image.

Then open your GitHub repository:

**Settings → Secrets and variables → Actions**

**A. Configure repository variables**

Under the **Variables** tab, add:

| Variable | Example value |
|---|---|
| `ENABLE_DOCKERHUB_PUBLISHING` | `true` |
| `DOCKERHUB_IMAGE` | `yourusername/windows-linux-server-monitor:latest` |

Replace the example image name with your own Docker Hub username and repository.

Set `ENABLE_DOCKERHUB_PUBLISHING` to `false` if you only want to build and validate the Docker image without publishing it.

**B. Configure repository secrets**

Under the **Secrets** tab, add:

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username. |
| `DOCKERHUB_TOKEN` | Your Docker Hub access token. |

Create an access token through your Docker Hub account and use it instead of your account password.

**Security:** Never put actual credentials or access tokens in the workflow file, README, or source code. Store them only as GitHub Actions secrets.

**C. Push changes to main**

After configuring the variables and secrets, merge your changes into `main` and push updates to that branch.

When publishing is enabled, GitHub Actions authenticates with Docker Hub using the configured repository secrets and pushes the image to the configured Docker Hub repository.

You do not need to run `docker login` on your local machine for this automated process.

### Local Docker login vs. GitHub Actions login

There are two separate authentication processes.

**Manual publishing from your computer**

If you build and push an image manually from your local machine, you must authenticate with Docker Hub first.

For example, when using Ubuntu through WSL:

```bash
docker login
```

Then tag and push your image:

```bash
docker tag windows-linux-server-monitor-monitor:latest yourusername/windows-linux-server-monitor:latest

docker push yourusername/windows-linux-server-monitor:latest
```

For this process, Docker authentication is handled locally by Docker. The login performed through Ubuntu WSL allows the local Docker client to push images to Docker Hub.

**Automated publishing through GitHub Actions**

GitHub Actions handles Docker Hub authentication using the repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

The workflow uses these secrets in its Docker login step. GitHub Actions performs the login on its own runner, independently of the user's local Docker login.

You do not need to log in through Ubuntu WSL to enable automated publishing.

### Publishing behavior

| Situation | Tests | Docker build | Docker Hub publishing |
|---|---|---|---|
| Pull request targeting `main` | Yes | Yes | No |
| Push to `main`, publishing enabled | Yes | Yes | Yes |
| Push to `main`, publishing disabled | Yes | Yes | No |
| Fork or clone without Docker Hub credentials | Yes | Yes | No |

The workflow uses the following conditions:

- The Docker build job must wait for the cross-platform test job to succeed.
- The Docker login step runs only when publishing is enabled and the event is a push to `main`.
- The image is pushed only when publishing is enabled and the event is a push to `main`.
- Pull requests build and validate the image without publishing it.

Publishing can be controlled without modifying the workflow code:

- Set `ENABLE_DOCKERHUB_PUBLISHING` to `true` to enable publishing.
- Set it to `false` to disable publishing while keeping tests and Docker build validation active.

The image destination can also be changed using `DOCKERHUB_IMAGE`.

**Note for developers using a fork or clone:**

GitHub Actions workflows are included when the repository is cloned or forked. However, repository secrets and variables are not copied from the original repository.

The workflow can still run tests and validate Docker builds without Docker Hub credentials. Developers who want to publish their own images must configure their own repository variables, Docker Hub repository, and GitHub Actions secrets.

## Resource Simulation

The project includes `simulator.py` to generate temporary system resource usage for testing.

The simulator:

- Generates CPU load using a separate process.
- Allocates 256 MB of RAM.
- Creates a temporary 100 MB disk file.
- Runs the simulation for 20 seconds.
- Terminates the CPU process, releases allocated memory, and removes the temporary file after execution.

Run the simulator:

```bash
python simulator.py
```

While the simulator is running, execute `monitor.py` separately to observe resource usage.

### Windows simulation test results

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

## Git Workflow

For future development, create a separate branch from the updated `main` branch:

```bash
git switch main
git pull origin main
git switch -c feature/your-feature
```

Stage and commit changes:

```bash
git add .
git commit -m "Describe your changes"
```

Push the new branch:

```bash
git push -u origin feature/your-feature
```

Open a Pull Request targeting `main`.

After the Pull Request is reviewed and merged, synchronize your local main branch:

```bash
git switch main
git pull origin main
```

The project uses branch protection and required GitHub Actions checks for the Ubuntu and Windows test jobs.

## Limitations

- Monitoring results depend on the operating system and environment where the tool is executed.
- Docker containers monitor their visible container environment by default, not the entire host machine.
- Automated execution under WSL2 depends on the WSL environment remaining active.
- The simulator generates temporary resource usage for testing and does not represent actual production workloads.
- Linux simulator testing has not yet been performed.