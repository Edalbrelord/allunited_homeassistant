from dateutil import parser

import json
import re

from .types import AllUnitedReservation


class AllUnitedApi:
    """AllUnited API to fetch data from Planningboard"""

    def __init__(self) -> None:
        """Initialize AllUnited API"""

    async def get_events(self) -> list[AllUnitedReservation]:

        # json = self._parse_html(html)
        # events = self._parse_events(json)

        events = []
        return events

    def _parse_html(self, html: str):
        """Retrieves the JSON object with reservations from the HTML

        The HTML contains a JSON object with the reservations entered as parameters in a JS script.
        """

        regexp = 'new Timeline\((?P<reservations>{.*}), (\[{.*}\]), ({.*}), ({.*})\);'
        match = re.search(regexp, html, re.M | re.S)

        reservations_json = match.group(1)
        reservations = json.loads(reservations_json)

        return reservations

    def _parse_events(self, json) -> list[AllUnitedReservation]:
        """Creates AllUnitedEvents from the json data"""
        reservations: list[AllUnitedReservation] = []
        for key in json:
            court = json[key]
            for reservation_raw in court:
                # TODO: Timezone from config
                timezones = {None: "Europe/Amsterdam"}

                start_raw = f"{reservation_raw["datefrom"]} {reservation_raw["timefrom"]}"
                event_start = parser.parse(
                    start_raw, yearfirst=True, tzinfos=timezones
                )

                end_raw = f"{reservation_raw["dateto"]} {reservation_raw["timeto"]}"
                event_end = parser.parse(
                    end_raw, yearfirst=True, tzinfos=timezones
                )

                reservation = AllUnitedReservation(
                    reservation_id=reservation_raw["reservationId"],
                    location=reservation_raw["locationcode"],
                    start=event_start,
                    end=event_end
                )
                reservations.append(reservation)

        return reservations
