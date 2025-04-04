from dataclasses import dataclass
from datetime import datetime


@dataclass
class AllUnitedReservation:
    """Reservation based on AllUnited Planningboard"""
    reservation_id: str
    location: str
    start: datetime
    end: datetime


@dataclass
class AllUnitedReservationsData:
    courts: list[str]
    reservations: list[AllUnitedReservation]
