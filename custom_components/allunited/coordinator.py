import logging
from datetime import timedelta
import async_timeout

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)
from homeassistant.util import dt as dt_util
from homeassistant.components.calendar import (
    CalendarEvent,
)

_LOGGER = logging.getLogger(__name__)


class AllUnitedCoordinator(DataUpdateCoordinator[CalendarEvent]):
    """AllUnited update coordinator."""

    def __init__(self, hass, config_entry):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="AllUnited Planningboard",
            config_entry=config_entry,
            update_interval=timedelta(seconds=30),
            always_update=True  # False if __eq__ is available
        )

        # TODO: my_api thingy with url?
        # self.my_api = my_api
        # self._device: MyDevice | None = None

    async def _async_setup(self):
        """Set up Coordinator, called from async_config_entry_first_refresh()"""

    async def _async_update_data(self):
        """Fetch data from the endpoint

        Data will be saved in lookup tables and is available from coordinator.data[]?
        """

        _LOGGER.debug("Fetching data")
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                now = dt_util.now()
                sample_event1: CalendarEvent = CalendarEvent(
                    start=now,
                    end=now + timedelta(hours=1),
                    summary="Testing 1"
                )
                sample_event2: CalendarEvent = CalendarEvent(
                    start=now,
                    end=now + timedelta(hours=1),
                    summary="Testing 2"
                )

                return [sample_event1, sample_event2]

        # except ApiAuthError as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            # raise ConfigEntryAuthFailed from err
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
