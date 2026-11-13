from monitor import check_cpu_alert, check_disk_alert, check_ram_alert


def test_cpu_below_threshold():
    result = check_cpu_alert(50)

    assert result == "CPU usage is in normal condition."


def test_cpu_at_threshold():
    result = check_cpu_alert(80)

    assert result == "WARNING: CPU usage is above the threshold!"


def test_ram_below_threshold():
    result = check_ram_alert(50)

    assert result == "RAM usage is in normal condition."


def test_ram_at_threshold():
    result = check_ram_alert(80)

    assert result == "WARNING: RAM usage is above the threshold!"


def test_disk_below_threshold():
    result = check_disk_alert(50)

    assert result == "Disk usage is in normal condition."


def test_disk_at_threshold():
    result = check_disk_alert(90)

    assert result == "Disk usage is above the threshold!"
