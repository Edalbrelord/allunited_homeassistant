from .const import DOMAIN
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
            vol.Required("name"): str,
            vol.Required("url"): str
        }

        if user_input is not None:
            return self.async_create_entry(
                title=f"AllUnited - {user_input["name"]}",
                data={
                    "url": user_input["url"],
                }
            )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema)
        )
