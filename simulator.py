import multiprocessing
import os
import tempfile
import time
from pathlib import Path


# Simulation settings
DURATION = 20
MEMORY_MB = 256
DISK_MB = 100


def generate_cpu_load(duration):
    end_time = time.monotonic() + duration
    value = 0

    while time.monotonic() < end_time:
        value += 1


def main():
    cpu_process = multiprocessing.Process(target=generate_cpu_load, args=(DURATION,))

    temp_file_path = None
    memory_load = None

    try:
        print("Starting resource simulation...")

        # Generate CPU load
        cpu_process.start()

        # Generate RAM usage
        print(f"Allocating {MEMORY_MB} MB of RAM...")
        memory_load = bytearray(MEMORY_MB * 1024 * 1024)

        # Generate disk usage
        print(f"Creating {DISK_MB} MB temporary file...")

        file_descriptor, temp_file_path = tempfile.mkstemp(
            prefix="monitor_simulation_", suffix=".tmp"
        )

        with os.fdopen(file_descriptor, "wb") as temp_file:
            block = b"0" * (1024 * 1024)

            for _ in range(DISK_MB):
                temp_file.write(block)

            temp_file.flush()
            os.fsync(temp_file.fileno())

        print(f"Simulation running for {DURATION} seconds...")

        time.sleep(DURATION)

    finally:
        # Stop CPU process
        if cpu_process.is_alive():
            cpu_process.terminate()

        cpu_process.join()

        # Release RAM
        del memory_load

        # Remove temporary disk file
        if temp_file_path:
            Path(temp_file_path).unlink(missing_ok=True)

        print("Resource simulation completed.")
        print("Temporary resources cleaned up.")


if __name__ == "__main__":
    main()
