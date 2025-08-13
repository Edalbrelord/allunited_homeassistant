from dataclasses import dataclass
from datetime import datetime


@dataclass
class AllUnitedCourt:
    """Reservation based on AllUnited Planningboard"""
    id: str
    name: str
    type: str


@dataclass
class AllUnitedReservation:
    """Reservation based on AllUnited Planningboard"""
    reservation_id: str
    location: str
    start: datetime
    end: datetime


@dataclass
class AllUnitedReservationsData:
    timestamp: datetime
    courts: list[AllUnitedCourt]
    reservations: list[AllUnitedReservation]
