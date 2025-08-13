from pytz import timezone
from custom_components.allunited.allunited_api import AllUnitedApi

from pathlib import Path


def test_parse_html():
    html = _load_fixture("example.html")

    api = AllUnitedApi("empty", tz=timezone("Europe/Amsterdam"))
    (json_events, json_courts) = api._parse_html(html)

    # 24 Tennis courts are listed in the sample data
    assert len(json_events) == 24
    assert len(json_courts) == 29


def test_parse_events():
    html = _load_fixture("example.html")

    api = AllUnitedApi("empty", tz=timezone("Europe/Amsterdam"))
    (json_events, _) = api._parse_html(html)
    events = api._parse_events(json_events)

    assert len(events) == 82

    reservation = events[0]
    assert reservation.reservation_id == "71170453"
    assert reservation.start.isoformat() == "2025-04-01T09:00:00+02:00"


def test_parse_events_is_ordered():
    html = _load_fixture("example.html")

    api = AllUnitedApi("empty", tz=timezone("Europe/Amsterdam"))
    (json_events, _) = api._parse_html(html)
    events = api._parse_events(json_events)

    reservation_1 = events[0]
    reservation_2 = events[1]

    assert reservation_1.start <= reservation_2.start


def test_parse_courts():
    html = _load_fixture("example.html")

    api = AllUnitedApi("empty", tz=timezone("Europe/Amsterdam"))
    (_, json_courts) = api._parse_html(html)
    courts = api._parse_courts(json_courts)

    assert len(courts) == 29


def _load_fixture(filename: str) -> str:
    """Load a fixture."""
    path = Path(__package__) / "fixtures" / filename
    return path.read_text(encoding="utf-8")
