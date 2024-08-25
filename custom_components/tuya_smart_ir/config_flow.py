import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from .const import (
    DOMAIN,
    CLIENT,
    CONF_INFRARED_ID,
    CONF_DEVICE_ID,
    CONF_ENTITY_DATA
)
from .api import TuyaAPI


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
    
    async def async_step_user(self, user_input):
        errors = {}

        domain_config  = self.hass.data.get(DOMAIN, {})
        client = domain_config.get(CLIENT, None)
        if client is None:
            return self.async_abort(reason="credentials")

        if user_input is not None:
            infrared_id = user_input.get(CONF_INFRARED_ID)
            device_id = user_input.get(CONF_DEVICE_ID)
            
            response = await TuyaAPI(self.hass, client).async_fetch_commands(infrared_id, device_id)
            if response:
                user_input[CONF_ENTITY_DATA] = response
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            
            errors["base"] = "connection"

        data_schema = vol.Schema(required_data())
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)


def required_data():
    return {
        vol.Required(CONF_INFRARED_ID): cv.string,
        vol.Required(CONF_DEVICE_ID): cv.string,
        vol.Required(CONF_NAME): cv.string
    }