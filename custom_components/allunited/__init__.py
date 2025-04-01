"""The AllUnited integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import AllUnitedCoordinator

CONFIG_SCHEMA = vol.Schema({vol.Optional(DOMAIN): {}}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the AllUnited integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AllUnited from a config entry."""

    # Store config entry data
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # TODO: Where to configure API / URL thingy? __init__.py can store it in hass.data apparently..

    coordinator = AllUnitedCoordinator(hass, config_entry=entry)
    entry.runtime_data = coordinator

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.CALENDAR])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    # Remove stored data
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    # Unload the sensor platform
    # await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    return True
