"""Tests for cross-platform scheduler."""
from unittest.mock import patch


def test_detect_platform_macos():
    from pipeline.scheduler import detect_platform
    with patch("platform.system", return_value="Darwin"):
        assert detect_platform() == "macos"


def test_detect_platform_linux():
    from pipeline.scheduler import detect_platform
    with patch("platform.system", return_value="Linux"):
        assert detect_platform() == "linux"


def test_detect_platform_unsupported():
    from pipeline.scheduler import detect_platform
    with patch("platform.system", return_value="Windows"):
        assert detect_platform() == "unsupported"


def test_launchd_plist_content():
    from pipeline.scheduler import _launchd_plist_content
    content = _launchd_plist_content("/path/to/run.sh", "06:00")
    assert "com.claude-news" in content
    assert "/path/to/run.sh" in content
    assert "<integer>6</integer>" in content
    assert "<integer>0</integer>" in content


def test_launchd_plist_custom_time():
    from pipeline.scheduler import _launchd_plist_content
    content = _launchd_plist_content("/path/to/run.sh", "14:30")
    assert "<integer>14</integer>" in content
    assert "<integer>30</integer>" in content


def test_systemd_unit_content():
    from pipeline.scheduler import _systemd_service_content, _systemd_timer_content
    service = _systemd_service_content("/path/to/run.sh")
    assert "ExecStart=/path/to/run.sh" in service
    timer = _systemd_timer_content("06:00")
    assert "OnCalendar=*-*-* 06:00:00" in timer


def test_crontab_entry():
    from pipeline.scheduler import _crontab_entry
    entry = _crontab_entry("/path/to/run.sh", "06:00")
    assert entry == "0 6 * * * /path/to/run.sh  # claude-news"


def test_crontab_entry_custom_time():
    from pipeline.scheduler import _crontab_entry
    entry = _crontab_entry("/path/to/run.sh", "14:30")
    assert entry == "30 14 * * * /path/to/run.sh  # claude-news"
