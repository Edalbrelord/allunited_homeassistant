from dataclasses import dataclass
from datetime import datetime
from homeassistant.config_entries import ConfigEntry

from .coordinator import AllUnitedCoordinator

type AllUnitedConfigEntry = ConfigEntry[AllUnitedCoordinator]


@dataclass
class AllUnitedEvent:
    """Event based on AllUnited Planningboard"""
    reservation_id: str
    description: str
    start_time: datetime
    end_time: datetime
