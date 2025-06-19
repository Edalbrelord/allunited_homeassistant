from typing import Any
import voluptuous as vol

from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, ConfigEntry, ConfigSubentryFlow, SubentryFlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    SelectOptionDict
)

from .const import CONF_CALENDAR_COURTS, DOMAIN, CONF_CALENDAR_NAME, CONF_CALENDAR_URL
from .types import AllUnitedReservationsData


class AllunitedConfigFlow(ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    @classmethod
    @callback
    def async_get_supported_subentry_types(
        cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        """Return subentries supported by this integration."""
        return {"calendar": CalendarSubentryFlowHandler}

    async def async_step_user(self, user_input):
        data_schema = {
            vol.Required(CONF_CALENDAR_NAME): str,
            vol.Required(CONF_CALENDAR_URL): str
        }

        if user_input is not None:
            return self.async_create_entry(
                title=f"AllUnited - {user_input[CONF_CALENDAR_NAME]}",
                data={
                    "name": user_input[CONF_CALENDAR_NAME],
                    "url": user_input[CONF_CALENDAR_URL],
                }
            )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema)
        )

    async def async_step_reconfigure(self, user_input):
        data_schema = {
            vol.Required(CONF_CALENDAR_NAME): str,
            vol.Required(CONF_CALENDAR_URL): str
        }

        if user_input is not None:
            return self.async_update_reload_and_abort(
                title=f"AllUnited - {user_input[CONF_CALENDAR_NAME]}",
                data={
                    "name": user_input[CONF_CALENDAR_NAME],
                    "url": user_input[CONF_CALENDAR_URL],
                }
            )

        return self.async_show_form(
            step_id="reconfigure", data_schema=vol.Schema(data_schema)
        )


class CalendarSubentryFlowHandler(ConfigSubentryFlow):
    """Handle subentry flow for adding and modifying a calendar."""

    async def get_data_schema(self, coordinator) -> vol.Schema:

        data: AllUnitedReservationsData = coordinator.data

        options: list[SelectOptionDict] = []
        for court in data.courts:
            option = SelectOptionDict(label=court.name, value=court.id)
            options.append(option)

        data_schema = vol.Schema({
            vol.Required(CONF_CALENDAR_NAME): str,
            vol.Required(CONF_CALENDAR_COURTS): SelectSelector(
                config=SelectSelectorConfig(
                    multiple=True,
                    mode=SelectSelectorMode.LIST,
                    options=options,
                ),
            ),
        })

        return data_schema

    async def async_step_user(
        self, user_input
    ) -> SubentryFlowResult:
        """User flow to add a new calendar for a group of courts.

        When a subentry is saved, reload the integration to trigger the setup again.
        """

        configuration_data = self.hass.data[DOMAIN][self._entry_id]
        coordinator = configuration_data.coordinator

        data_schema = self.get_data_schema(coordinator)

        if user_input is not None:
            return self.async_create_entry(
                title=f"AllUnited - {user_input[CONF_CALENDAR_NAME]}",
                data={
                    "name": user_input[CONF_CALENDAR_NAME],
                    "courts": user_input[CONF_CALENDAR_COURTS],
                }
            )

        return self.async_show_form(
            step_id="user", data_schema=data_schema
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> SubentryFlowResult:
        """User flow to modify an existing location."""
        config_entry = self._get_entry()
        # Retrieve the specific subentry targeted for update.
        config_subentry = self._get_reconfigure_subentry()

        if user_input is not None:
            return self.async_update_and_abort(
                config_entry,
                config_subentry,
                title=f"AllUnited - {user_input[CONF_CALENDAR_NAME]}",
                data={
                    "name": user_input[CONF_CALENDAR_NAME],
                    "courts": user_input[CONF_CALENDAR_COURTS],
                }
            )

        configuration_data = self.hass.data[DOMAIN][self._entry_id]
        coordinator = configuration_data.coordinator

        data_schema = await self.get_data_schema(coordinator)

        return self.async_show_form(
            step_id="reconfigure", data_schema=data_schema
        )
