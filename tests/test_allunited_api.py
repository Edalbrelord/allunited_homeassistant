from custom_components.allunited.allunited_api import AllUnitedApi

from pathlib import Path


def load_fixture(filename: str) -> str:
    """Load a fixture."""
    path = Path(__package__) / "fixtures" / filename
    return path.read_text(encoding="utf-8")


async def test_retrieve_events():
    api = AllUnitedApi()
    events = await api.get_events()

    assert events == []


def test_parse_html():
    html = ""

    api = AllUnitedApi()
    events = api._parse_html(html)

    assert events == []
