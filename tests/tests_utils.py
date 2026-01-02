import pytest
from modules.utils import format_time

@pytest.mark.parametrize(
    "ms, expected",
    [
        (0, "00:00"),
        (999, "00:00"),
        (1000, "00:01"),
        (61000, "01:01"),
        (3600000, "60:00"),  # 1 hour → 60 minutes
    ]
)
def test_format_time_parametrized(ms, expected):
    assert format_time(ms) == expected


def test_format_time_large_value():
    # 2 hours, 30 minutes, 15 seconds → 150 minutes, 15 seconds
    ms = (2 * 3600 + 30 * 60 + 15) * 1000
    assert format_time(ms) == "150:15"


def test_format_time_negative_value():
    assert format_time(-1000) == "00:00"
