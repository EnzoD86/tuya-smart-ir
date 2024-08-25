import logging

_LOGGER = logging.getLogger(__package__)


class TuyaAPI:
    def __init__(self, hass, client):
        self._hass = hass
        self._client = client

    async def async_fetch_commands(self, infrared_id, device_id):
        try:
            url = f"/v2.0/infrareds/{infrared_id}/remotes/{device_id}/keys"
            _LOGGER.debug(f"API get_keys url: {url}")
            result = await self._hass.async_add_executor_job(self._client.get, url)
            _LOGGER.debug(f"API get_keys response: {str(result)}")
            if result.get("success"):
                return result.get("result")
            raise Exception(TuyaDetails(url, "", result).to_dict())
        except Exception as e:
            _LOGGER.error(f"Error fetching keys for device {device_id}: {e}")
            raise Exception(e)

    async def async_send_command(self, infrared_id, device_id, category_id, key_id, key):
        try:
            url = f"/v2.0/infrareds/{infrared_id}/remotes/{device_id}/raw/command"
            _LOGGER.debug(f"API send_command url: {url}")
            command = { "category_id": category_id, "key_id": key_id, "key": key }
            _LOGGER.debug(f"API send_command request: {command}")
            result = await self._hass.async_add_executor_job(self._client.post, url, command)
            _LOGGER.debug(f"API send_command response: {str(result)}")
            if not result.get("success"):
                raise Exception(TuyaDetails(url, command, result).to_dict())
        except Exception as e:
            _LOGGER.error(f"Error sending command to device {device_id}: {e}")
            raise Exception(e)


class TuyaDetails(object):
    def __init__(self, url, request, response):
        self.url = url
        self.request = request
        self.response = response
        
    def to_dict(self):
        return vars(self)
