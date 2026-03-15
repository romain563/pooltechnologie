"""Intégration PoolTechnologie."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL, CONF_REGULATION_ORP
from .modbus import PoolTechnologieModbusClient
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Configure PoolTechnologie à partir d'une entrée de configuration."""
    hass.data.setdefault(DOMAIN, {})

    modbus_client = PoolTechnologieModbusClient(entry.data["ip"], entry.data["port"], entry.data["unit_id"])
    try:
        modbus_client.connect()
    except ConnectionError as e:
        _LOGGER.error("Erreur de connexion : %s", e)
        return False

    coordinator = PoolTechnologieDataUpdateCoordinator(hass, modbus_client, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "modbus_client": modbus_client,
        "options": entry.options,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Désactive une entrée de configuration."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        modbus_client = hass.data[DOMAIN][entry.entry_id]["modbus_client"]
        modbus_client.close()
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class PoolTechnologieDataUpdateCoordinator(DataUpdateCoordinator):
    """Classe pour gérer la récupération des données depuis l'appareil Modbus."""

    def __init__(self, hass, modbus_client, entry):
        """Initialise le coordinateur."""
        self.modbus_client = modbus_client
        self.entry = entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Récupère les données depuis l'appareil Modbus."""
        try:
            data = {}
            for sensor_key, sensor_config in SENSORS.items():
                value = self.modbus_client.read_register(sensor_config["address"])
                if value is not None:
                    data[sensor_key] = value * sensor_config["scale"]

            for config_key, config_config in CONFIG_ENTITIES.items():
                value = self.modbus_client.read_register(config_config["address"])
                if value is not None:
                    data[config_key] = value * config_config.get("scale", 1)

            return data
        except Exception as e:
            raise UpdateFailed(f"Erreur de mise à jour : {e}")
