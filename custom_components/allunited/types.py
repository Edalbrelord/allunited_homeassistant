from homeassistant.config_entries import ConfigEntry

from .coordinator import AllUnitedCoordinator

type AllUnitedConfigEntry = ConfigEntry[AllUnitedCoordinator]
