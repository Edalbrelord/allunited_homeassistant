from custom_components.allunited.allunited_api import AllUnitedApi

from pathlib import Path


async def test_retrieve_events():
    api = AllUnitedApi()
    events = await api.get_events()

    assert events == []


def test_parse_html():
    html = _load_fixture("example.html")

    api = AllUnitedApi()
    json_events = api._parse_html(html)

    # 24 Tennis courts are listed in the sample data
    assert len(json_events) == 24


def test_parse_events():
    html = _load_fixture("example.html")

    api = AllUnitedApi()
    json_events = api._parse_html(html)
    events = api._parse_events(json_events)

    assert len(events) == 82

    reservation = events[0]
    assert reservation.summary == "71169946"
    assert reservation.start.isoformat() == "2025-04-01T20:15:00+00:00"


def _load_fixture(filename: str) -> str:
    """Load a fixture."""
    path = Path(__package__) / "fixtures" / filename
    return path.read_text(encoding="utf-8")
