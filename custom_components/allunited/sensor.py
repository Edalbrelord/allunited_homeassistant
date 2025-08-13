"""Platform for sensor integration."""
from __future__ import annotations
import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorEntityDescription
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.util import dt as dt_util

from .const import DOMAIN, CONF_CALENDAR_NAME, CONF_CALENDAR_COURTS
from .types import AllUnitedReservation, AllUnitedReservationsData
from .coordinator import AllUnitedCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the AllUnited sensor platform."""
    coordinator = config_entry.runtime_data

    # Create calendar with all events
    name = config_entry.data[CONF_CALENDAR_NAME]
    allunited_date_sensor = AllUnitedDateSensor(
        coordinator,
        name,
        unique_id=config_entry.entry_id,
    )

    sensor_entities = [allunited_date_sensor]

    async_add_entities(sensor_entities, True)


class AllUnitedDateSensor(CoordinatorEntity[AllUnitedCoordinator], SensorEntity):
    """Representation of a Sensor."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    entity_description = SensorEntityDescription(
        key="date_sensor",
    )

    def __init__(
        self,
        coordinator,
        idx,
        unique_id: str
    ):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
        self._attr_unique_id = unique_id
        self._attr_translation_key = "date_sensor"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _timestamp: datetime.datetime = self.coordinator.data.timestamp
        local_timestamp = _timestamp.replace(tzinfo=dt_util.get_default_time_zone())
        self._attr_native_value = local_timestamp

        self.async_write_ha_state()
