"""Provide info to system health."""

from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, CONF_CALENDAR_URL


@callback
def async_register(hass: HomeAssistant, register: system_health.SystemHealthRegistration) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass: HomeAssistant):
    """Get info for the info page."""
    config_entry: ConfigEntry = hass.config_entries.async_entries(DOMAIN)[0]
    endpoint = config_entry.data[CONF_CALENDAR_URL]

    return {
        "can_reach_server": system_health.async_check_can_reach_url(hass, endpoint),
    }
