
import logging
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
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

from .const import DOMAIN, CONF_CALENDAR_NAME, CONF_CALENDAR_COURTS
from .types import AllUnitedReservation, AllUnitedReservationsData
from .coordinator import AllUnitedCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the AllUnited calendar platform."""
    coordinator = config_entry.runtime_data

    # Create calendar with all events
    name = config_entry.data[CONF_CALENDAR_NAME]
    entity = AllUnitedCalendarEntity(
        coordinator,
        name,
        courts=None,
        unique_id=config_entry.entry_id,
    )

    calendars: list[AllUnitedCalendarEntity] = [entity]
    for subentry_id in config_entry.subentries:
        # Create calendar for group contained in subentry
        subentry = config_entry.subentries[subentry_id]
        group_entity = AllUnitedCalendarEntity(
            coordinator,
            name=subentry.data[CONF_CALENDAR_NAME],
            courts=subentry.data[CONF_CALENDAR_COURTS],
            unique_id=subentry_id
        )
        calendars.append(group_entity)

        _LOGGER.debug(
            f"Creating group calendar for {subentry.data[CONF_CALENDAR_NAME]}, courts: {subentry.data[CONF_CALENDAR_COURTS]}"
        )

    async_add_entities(calendars, True)


class AllUnitedCalendarEntity(CoordinatorEntity[AllUnitedCoordinator], CalendarEntity):
    """A calendar entity based on reservations from AllUnited."""
    _event: CalendarEvent | None = None
    _courts: list[str] | None = None

    def __init__(
        self,
        coordinator: AllUnitedCoordinator,
        name: str,
        courts: list[str] | None,
        unique_id: str,
    ) -> None:
        """Initialize AllUnitedCalendarEntity."""
        super().__init__(coordinator)
        self._courts = courts
        self._attr_name = name
        self._attr_unique_id = unique_id

    # Coordinator Implementation
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        # formatted_data = pprint.pformat(self.coordinator.data)
        # _LOGGER.debug(f"Received data from coordinator:\n{formatted_data}")

        # todo, retrieve active event...

        data: AllUnitedReservationsData = self.coordinator.data
        reservations = self.filter_by_courts(
            reservations=data.reservations, courts=self._courts)

        next_reservation = next(iter(reservations), None)
        if next_reservation is not None:
            next_event = self.create_calendar_event(next_reservation)
            self._event = next_event

        super()._handle_coordinator_update()

    # Calendar Implementation
    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        return self._event

    # async def async_update(self) -> None:
    #    """Update entity state with the next upcoming event."""

    #    _LOGGER.debug("Updating Allunited Calendar")

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""

        _LOGGER.debug("Getting events")

        data: AllUnitedReservationsData = self.coordinator.data
        events: list[CalendarEvent] = []

        reservations = self.filter_by_courts(
            reservations=data.reservations, courts=self._courts)

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

    def filter_by_courts(self, reservations: list[AllUnitedReservation], courts: list[str]) -> list[AllUnitedReservation]:
        filtered_reservations = []
        if courts is not None:
            filtered_reservations = [
                i for i in reservations if i.location in courts]
        else:
            filtered_reservations = reservations

        return filtered_reservations
