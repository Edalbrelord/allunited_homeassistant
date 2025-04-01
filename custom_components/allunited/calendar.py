
import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN, CONF_CALENDAR_NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the AllUnited calendar platform."""

    name = config_entry.data[CONF_CALENDAR_NAME]
    entity = AllUnitedCalendarEntity(
        name=name,
        unique_id=config_entry.entry_id,
    )

    async_add_entities([entity], True)


class AllUnitedCalendarEntity(CalendarEntity):
    """A calendar entity based on reservations from AllUnited."""
    _event: CalendarEvent | None = None

    def __init__(
        self,
        name: str,
        unique_id: str,
    ) -> None:
        """Initialize AllUnitedCalendarEntity."""

        self._attr_name = name
        self._attr_unique_id = unique_id

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        return self._event

    async def async_update(self) -> None:
        """Update entity state with the next upcoming event."""

        _LOGGER.debug("Updating Allunited Calendar")

        now = dt_util.now()
        sample_event: CalendarEvent = CalendarEvent(
            start=now,
            end=now + timedelta(hours=1),
            summary="Test!"
        )
        events = [sample_event]

        self._event = sample_event

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""

        _LOGGER.debug("Getting events")

        now = dt_util.now()
        sample_event: CalendarEvent = CalendarEvent(
            start=now,
            end=now + timedelta(hours=1),
            summary="Testing?"
        )
        event_list: list[CalendarEvent] = [sample_event]

        return event_list
