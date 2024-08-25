from homeassistant.const import Platform

DOMAIN = "tuya_smart_ir"
MANUFACTURER = "Tuya"
CLIENT = "CLIENT"
SERVICE = "SERVICE"
PLATFORMS = [Platform.BUTTON]

CONF_ACCESS_ID = "access_id"
CONF_ACCESS_SECRET = "access_secret"
CONF_TUYA_COUNTRY = "country"
CONF_INFRARED_ID = "infrared_id"
CONF_DEVICE_ID = "device_id"
CONF_ENTITY_DATA = "entity_data"
CONF_KEY_LIST = "key_list"
CONF_KEY = "key"
CONF_KEY_ID = "key_id"
CONF_KEY_NAME = "key_name"
CONF_CATEGORY_ID = "category_id"


TUYA_ENDPOINTS = {
    "EU": "https://openapi.tuyaeu.com",
    "US": "https://openapi.tuyaus.com",
    "IN": "https://openapi.tuyain.com",
    "CN": "https://openapi.tuyacn.com"
}