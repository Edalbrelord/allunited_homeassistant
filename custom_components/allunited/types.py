from dataclasses import dataclass
from datetime import datetime
from homeassistant.config_entries import ConfigEntry

from .coordinator import AllUnitedCoordinator

type AllUnitedConfigEntry = ConfigEntry[AllUnitedCoordinator]


@dataclass
class AllUnitedReservation:
    """Reservation based on AllUnited Planningboard"""
    reservation_id: str
    location: str
    start: datetime
    end: datetime
