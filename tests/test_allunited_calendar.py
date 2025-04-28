import logging
from freezegun import freeze_time

from pytest_homeassistant_custom_component.common import MockConfigEntry

from datetime import datetime
from unittest.mock import Mock, patch
from homeassistant.core import HomeAssistant

from custom_components.allunited.coordinator import AllUnitedCoordinator
from custom_components.allunited.calendar import AllUnitedCalendarEntity
from custom_components.allunited.const import DOMAIN


async def test_empty_get_events(hass: HomeAssistant, empty_reservations_data):
    coordinator = Mock(spec=AllUnitedCoordinator)
    coordinator.data = empty_reservations_data

    calendar = AllUnitedCalendarEntity(coordinator, "Test", courts=None, unique_id="test_1")

    start_date = datetime.now()
    end_date = datetime.now()

    events = await calendar.async_get_events(hass, start_date, end_date)
    assert len(events) == 0


@patch('homeassistant.helpers.update_coordinator.BaseCoordinatorEntity._handle_coordinator_update')
@freeze_time("2025-04-28T10:00:00Z")
async def test_coordinator_update(mock_super, hass: HomeAssistant, reservations_data):
    coordinator = Mock(spec=AllUnitedCoordinator)
    coordinator.data = reservations_data

    calendar = AllUnitedCalendarEntity(coordinator, "Test", courts=None, unique_id="test_1")

    calendar._handle_coordinator_update()

    assert calendar._event is not None
    assert calendar._event.uid == "2"  # First event has ended

    mock_super.assert_called_once()  # Ensure CoordinatorEntity is also updated


@patch('homeassistant.helpers.update_coordinator.BaseCoordinatorEntity._handle_coordinator_update')
@freeze_time("2025-04-28T11:00:00Z")
async def test_coordinator_update_for_courts(mock_super, hass: HomeAssistant, reservations_data):
    coordinator = Mock(spec=AllUnitedCoordinator)
    coordinator.data = reservations_data

    calendar = AllUnitedCalendarEntity(coordinator, "Test", courts=["BAAN02"], unique_id="test_1")

    calendar._handle_coordinator_update()

    assert calendar._event is not None
    assert calendar._event.uid == "7"  # First two events for BAAN02 have ended


@patch('homeassistant.helpers.update_coordinator.BaseCoordinatorEntity._handle_coordinator_update')
@freeze_time("2025-04-28T11:00:00Z")
async def test_coordinator_update_no_upcoming_event(mock_super, hass: HomeAssistant, reservations_data):
    coordinator = Mock(spec=AllUnitedCoordinator)
    coordinator.data = reservations_data

    calendar = AllUnitedCalendarEntity(coordinator, "Test", courts=["BAAN03"], unique_id="test_1")

    calendar._handle_coordinator_update()

    assert calendar._event is None


async def test_court_filter_get_events(hass: HomeAssistant, reservations_data):
    coordinator = Mock(spec=AllUnitedCoordinator)
    coordinator.data = reservations_data

    calendar = AllUnitedCalendarEntity(coordinator, "Test", courts=["BAAN01"], unique_id="test_1")

    start_date = datetime.fromisoformat('2025-04-28T09:00:00Z')  # Applied to end_date, exclusive
    end_date = datetime.fromisoformat('2025-04-28T18:00:00Z')  # Applied to start_date, exclusive

    events = await calendar.async_get_events(hass, start_date, end_date)
    assert len(events) == 4


async def test_multiple_court_filter_get_events(hass: HomeAssistant, reservations_data):
    coordinator = Mock(spec=AllUnitedCoordinator)
    coordinator.data = reservations_data

    calendar = AllUnitedCalendarEntity(coordinator, "Test", courts=["BAAN01", "BAAN03"], unique_id="test_1")

    start_date = datetime.fromisoformat('2025-04-28T09:00:00Z')  # Applied to end_date, exclusive
    end_date = datetime.fromisoformat('2025-04-28T18:00:00Z')  # Applied to start_date, exclusive

    events = await calendar.async_get_events(hass, start_date, end_date)
    assert len(events) == 5


async def test_date_filter_get_events(caplog, hass: HomeAssistant, reservations_data):
    caplog.set_level(logging.DEBUG)

    coordinator = Mock(spec=AllUnitedCoordinator)
    coordinator.data = reservations_data

    calendar = AllUnitedCalendarEntity(coordinator, "Test", courts=None, unique_id="test_1")

    start_date = datetime.fromisoformat('2025-04-28T10:00:00Z')  # Applied to end_date, exclusive
    end_date = datetime.fromisoformat('2025-04-28T12:00:00Z')  # Applied to start_date, exclusive

    events = await calendar.async_get_events(hass, start_date, end_date)
    assert len(events) == 4
