"""Fixtures for AllUnited Integration"""
import pytest
from datetime import datetime

from custom_components.allunited.types import AllUnitedReservationsData, AllUnitedReservation, AllUnitedCourt


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    return


@pytest.fixture
def empty_reservations_data():
    """Return an empty reservations data object"""
    return AllUnitedReservationsData(
        courts=[],
        reservations=[]
    )


@pytest.fixture
def reservations_data():
    """Return a reservations data object with events and courts"""
    return AllUnitedReservationsData(
        courts=[
            AllUnitedCourt("BAAN01", "Baan 1", "GRV"),
            AllUnitedCourt("BAAN02", "Baan 2", "GRV"),
            AllUnitedCourt("BAAN03", "Baan 3", "SMC")
        ],
        reservations=[
            AllUnitedReservation("1", "BAAN01", datetime.fromisoformat("2025-04-28T09:00:00Z"), datetime.fromisoformat("2025-04-28T10:00:00Z")),
            AllUnitedReservation("2", "BAAN01", datetime.fromisoformat("2025-04-28T10:00:00Z"), datetime.fromisoformat("2025-04-28T11:00:00Z")),
            AllUnitedReservation("3", "BAAN01", datetime.fromisoformat("2025-04-28T11:00:00Z"), datetime.fromisoformat("2025-04-28T12:00:00Z")),
            AllUnitedReservation("4", "BAAN01", datetime.fromisoformat("2025-04-28T12:00:00Z"), datetime.fromisoformat("2025-04-28T13:00:00Z")),
            AllUnitedReservation("5", "BAAN02", datetime.fromisoformat("2025-04-28T09:00:00Z"), datetime.fromisoformat("2025-04-28T10:00:00Z")),
            AllUnitedReservation("6", "BAAN02", datetime.fromisoformat("2025-04-28T10:00:00Z"), datetime.fromisoformat("2025-04-28T11:00:00Z")),
            AllUnitedReservation("7", "BAAN02", datetime.fromisoformat("2025-04-28T11:00:00Z"), datetime.fromisoformat("2025-04-28T12:00:00Z")),
            AllUnitedReservation("8", "BAAN03", datetime.fromisoformat("2025-04-28T09:00:00Z"), datetime.fromisoformat("2025-04-28T10:00:00Z"))
        ]
    )
