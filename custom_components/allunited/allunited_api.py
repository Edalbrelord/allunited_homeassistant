import asyncio
from datetime import datetime as dt
from dateutil import parser
from pytz import timezone

import json
import re

from aiohttp import ClientSession, ClientConnectionError
from aiohttp.hdrs import METH_GET, METH_POST, METH_PUT, METH_DELETE

from .types import AllUnitedReservation, AllUnitedCourt, AllUnitedReservationsData


class AllUnitedApi:
    """AllUnited API to fetch data from Planningboard"""
    _url: str
    _session: ClientSession | None = None

    def __init__(self, url, tz: timezone) -> None:
        """Initialize AllUnited API"""
        self._url = url
        self._tz = tz

    async def get_data(self) -> AllUnitedReservationsData:

        if self._session is None:
            self._session = ClientSession()

        response = await self._session.request(
            METH_GET, self._url
        )

        html = await response.text()

        (json_events, json_courts) = self._parse_html(html)
        events = self._parse_events(json=json_events)
        courts = self._parse_courts(json=json_courts)

        data = AllUnitedReservationsData(
            timestamp=dt.now(tz=self._tz),
            courts=courts,
            reservations=events
        )

        return data

    def _parse_html(self, html: str):
        """Retrieves the JSON object with reservations from the HTML

        The HTML contains a JSON object with the reservations entered as parameters in a JS script.
        """

        regexp = 'new Timeline\((?P<reservations>{.*}), (\[{.*}\]), ({.*}), ({.*})\);'
        match = re.search(regexp, html, re.M | re.S)

        reservations_json = match.group(1)
        reservations = json.loads(reservations_json)

        courts_json = match.group(2)
        courts = json.loads(courts_json)

        return (reservations, courts)

    def _parse_events(self, json) -> list[AllUnitedReservation]:
        """Creates AllUnitedEvents from the json data"""
        reservations: list[AllUnitedReservation] = []
        for key in json:
            court = json[key]
            for reservation_raw in court:
                start_raw = f"{reservation_raw["datefrom"]} {reservation_raw["timefrom"]}"
                event_start = parser.parse(start_raw, yearfirst=True)

                end_raw = f"{reservation_raw["dateto"]} {reservation_raw["timeto"]}"
                event_end = parser.parse(end_raw, yearfirst=True)

                reservation = AllUnitedReservation(
                    reservation_id=reservation_raw["reservationId"],
                    location=reservation_raw["locationcode"],
                    start=self._tz.localize(event_start),
                    end=self._tz.localize(event_end)
                )

                reservations.append(reservation)

        return sorted(reservations, key=lambda reservation: reservation.start)

    def _parse_courts(self, json) -> list[AllUnitedCourt]:
        """Creates AllUnitedCourts from json data"""
        courts: list[AllUnitedCourt] = []

        for json_court in json:
            court = AllUnitedCourt(
                id=json_court["code"],
                name=json_court["name"],
                type=json_court["group"]
            )
            courts.append(court)

        return courts
