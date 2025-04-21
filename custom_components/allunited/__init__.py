"""The AllUnited integration."""

from __future__ import annotations
from dataclasses import dataclass
import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, CONF_CALENDAR_URL
from .coordinator import AllUnitedCoordinator
from .allunited_api import AllUnitedApi

CONFIG_SCHEMA = vol.Schema({vol.Optional(DOMAIN): {}}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)


@dataclass
class AllUnitedConfigurationData:
    """Configuration data set for AllUnited Integration"""
    coordinator: AllUnitedCoordinator
    url: str


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the AllUnited integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AllUnited from a config entry."""

    allunited_api = AllUnitedApi(url=entry.data[CONF_CALENDAR_URL])
    coordinator = AllUnitedCoordinator(
        hass, config_entry=entry, allunited_api=allunited_api)
    entry.runtime_data = coordinator

    configuration_data = AllUnitedConfigurationData(
        url=entry.data[CONF_CALENDAR_URL],
        coordinator=coordinator
    )
    hass.data[DOMAIN][entry.entry_id] = configuration_data

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.CALENDAR])
    return True


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating configuration from version %s.%s",
                  config_entry.version, config_entry.minor_version)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    # Remove stored data
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    # Unload the sensor platform
    # await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    return True
