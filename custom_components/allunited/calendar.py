
import logging
from datetime import datetime
import pprint

from homeassistant.core import HomeAssistant, callback
from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN, CONF_CALENDAR_NAME
from .types import AllUnitedConfigEntry, AllUnitedReservation
from .coordinator import AllUnitedCoordinator


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AllUnitedConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the AllUnited calendar platform."""
    coordinator = config_entry.runtime_data

    name = config_entry.data[CONF_CALENDAR_NAME]
    entity = AllUnitedCalendarEntity(
        coordinator,
        name,
        unique_id=config_entry.entry_id,
    )

    async_add_entities([entity], True)


class AllUnitedCalendarEntity(CoordinatorEntity[AllUnitedCoordinator], CalendarEntity):
    """A calendar entity based on reservations from AllUnited."""
    _event: CalendarEvent | None = None

    def __init__(
        self,
        coordinator: AllUnitedCoordinator,
        name: str,
        unique_id: str,
    ) -> None:
        """Initialize AllUnitedCalendarEntity."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = unique_id

    # Coordinator Implementation
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        formatted_data = pprint.pformat(self.coordinator.data)
        _LOGGER.debug(f"Received data from coordinator:\n{formatted_data}")

        self.async_write_ha_state()

    # Calendar Implementation
    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        return self._event

    async def async_update(self) -> None:
        """Update entity state with the next upcoming event."""

        _LOGGER.debug("Updating Allunited Calendar")

        reservations: list[AllUnitedReservation] = self.coordinator.data

        next_reservation = next(iter(reservations), None)
        next_event = self.create_calendar_event(next_reservation)
        self._event = next_event

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""

        _LOGGER.debug("Getting events")

        reservations: list[AllUnitedReservation] = self.coordinator.data
        events: list[CalendarEvent] = []

        for reservation in reservations:
            event = self.create_calendar_event(reservation)
            events.append(event)

        return events

    def create_calendar_event(self, reservation: AllUnitedReservation) -> CalendarEvent:
        event = CalendarEvent(
            start=reservation.start,
            end=reservation.end,
            summary=reservation.location,
            uid=reservation.reservation_id
        )
        return event
