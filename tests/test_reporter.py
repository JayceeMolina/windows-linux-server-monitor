import csv
import platform

from reporter import save_report


def test_save_report(tmp_path, monkeypatch):
    monkeypatch.setattr("reporter.__file__", str(tmp_path / "reporter.py"))

    save_report(45.5, 60.2, 90.1)

    folder = "windows" if platform.system() == "Windows" else "linux"
    csv_file = tmp_path / "reports" / folder / "data.csv"

    assert csv_file.is_file()

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        assert reader.fieldnames == [
            "timestamp",
            "cpu_usage",
            "ram_usage",
            "disk_usage",
        ]
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["cpu_usage"] == "45.5"
    assert rows[0]["ram_usage"] == "60.2"
    assert rows[0]["disk_usage"] == "90.1"


def test_save_report_append(tmp_path, monkeypatch):
    monkeypatch.setattr("reporter.__file__", str(tmp_path / "reporter.py"))

    # Create an initial report
    save_report(30.0, 40.0, 50.0)

    # Append another report
    save_report(60.0, 70.0, 80.0)

    folder = "windows" if platform.system() == "Windows" else "linux"
    csv_file = tmp_path / "reports" / folder / "data.csv"

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["cpu_usage"] == "30.0"
    assert rows[1]["cpu_usage"] == "60.0"
