import logging
from datetime import timedelta
from pathlib import Path
import async_timeout

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)

from .types import AllUnitedReservationsData
from .allunited_api import AllUnitedApi

_LOGGER = logging.getLogger(__name__)


class AllUnitedCoordinator(DataUpdateCoordinator):
    """AllUnited update coordinator."""
    _api: AllUnitedApi

    def __init__(self, hass, config_entry, allunited_api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="AllUnited Planningboard",
            config_entry=config_entry,
            update_interval=timedelta(seconds=30),
            always_update=True  # False if __eq__ is available
        )
        self._api = allunited_api

    async def _async_setup(self):
        """Set up Coordinator, called from async_config_entry_first_refresh()"""

    async def _async_update_data(self):
        """Fetch data from the endpoint

        Data will be saved in lookup tables and is available from coordinator.data
        """

        _LOGGER.debug("Fetching data")
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                data = await self._api.get_data()

                return data

        # except ApiAuthError as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            # raise ConfigEntryAuthFailed from err
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
