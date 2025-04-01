from .const import DOMAIN, CONF_CALENDAR_NAME, CONF_CALENDAR_URL
from homeassistant import config_entries

import voluptuous as vol


class AllunitedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

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
