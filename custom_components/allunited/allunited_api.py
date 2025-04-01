import asyncio
from .types import AllUnitedConfigEntry, AllUnitedEvent


class AllUnitedApi:
    """AllUnited API to fetch data from Planningboard"""

    def __init__(self) -> None:
        """Initialize AllUnited API"""

    async def get_events(self) -> list[AllUnitedEvent]:
        return []

    def _parse_html(self, html: str) -> list[AllUnitedEvent]:
        """Parses the HTML provided by the API

        The HTML contains a JSON object with the reservations entered as parameters in a JS script.
        """
        return []
