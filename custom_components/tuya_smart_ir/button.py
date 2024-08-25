import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.const import (
    CONF_NAME
)
from .const import (
    DOMAIN,
    MANUFACTURER,
    SERVICE,
    CONF_INFRARED_ID,
    CONF_DEVICE_ID,
    CONF_ENTITY_DATA,
    CONF_KEY_LIST,
    CONF_KEY,
    CONF_KEY_ID,
    CONF_KEY_NAME,
    CONF_CATEGORY_ID
)

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    entity_data = config_entry.data.get(CONF_ENTITY_DATA, {})
    async_add_entities(
        TuyaButton(hass, config_entry.data, idx) for idx, key_data in enumerate(entity_data.get(CONF_KEY_LIST, []))
    )


class TuyaButton(ButtonEntity):
    def __init__(self, hass, config, idx):
        self._service = hass.data.get(DOMAIN).get(SERVICE)
        self._infrared_id = config.get(CONF_INFRARED_ID)
        self._device_id = config.get(CONF_DEVICE_ID)
        self._name = config.get(CONF_NAME)

        entity_data = config.get(CONF_ENTITY_DATA, {})
        self._category_id = entity_data.get(CONF_CATEGORY_ID)

        key_data = entity_data.get(CONF_KEY_LIST, [])[idx]
        self._key = key_data.get(CONF_KEY)
        self._key_id = key_data.get(CONF_KEY_ID)
        self._key_name = key_data.get(CONF_KEY_NAME)

    @property
    def name(self):
        return self._key_name

    @property
    def unique_id(self):
        return self._key_id

    @property
    def device_info(self):
        return {
            "name": self._name,
            "identifiers": {(DOMAIN, self._name)},
            "via_device": (DOMAIN, self._infrared_id),
            "manufacturer": MANUFACTURER
        }

    async def async_press(self):
        await self._service.async_send_command(self._infrared_id, self._device_id, self._category_id, self._key_id , self._key)
