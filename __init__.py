"""Intégration PoolTechnologie."""
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL, SENSORS, CONFIG_ENTITIES
from .modbus import PoolTechnologieModbusClient
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure PoolTechnologie à partir d'une entrée de configuration."""
    hass.data.setdefault(DOMAIN, {})

    modbus_client = PoolTechnologieModbusClient(
        entry.data["ip"], entry.data["port"], entry.data["unit_id"]
    )

    try:
        await hass.async_add_executor_job(modbus_client.connect)
    except ConnectionError as e:
        raise ConfigEntryNotReady(f"Impossible de se connecter à l'appareil : {e}") from e

    coordinator = PoolTechnologieDataUpdateCoordinator(hass, modbus_client, entry)

    # CORRECTIF : si le premier refresh échoue (UpdateFailed), on convertit en
    # ConfigEntryNotReady pour que HA retente automatiquement au lieu de bloquer
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await hass.async_add_executor_job(modbus_client.close)
        raise

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "modbus_client": modbus_client,
        "options": entry.options,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Désactive une entrée de configuration."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        modbus_client = hass.data[DOMAIN][entry.entry_id]["modbus_client"]
        await hass.async_add_executor_job(modbus_client.close)
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class PoolTechnologieDataUpdateCoordinator(DataUpdateCoordinator):
    """Classe pour gérer la récupération des données depuis l'appareil Modbus."""

    def __init__(self, hass: HomeAssistant, modbus_client, entry: ConfigEntry) -> None:
        """Initialise le coordinateur."""
        self.modbus_client = modbus_client
        self.entry = entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)
            ),
        )

    async def _async_update_data(self) -> dict:
        """Récupère les données depuis l'appareil Modbus."""
        try:
            data = {}

            for sensor_key, sensor_config in SENSORS.items():
                value = await self.hass.async_add_executor_job(
                    self.modbus_client.read_register, sensor_config["address"]
                )
                if value is not None:
                    data[sensor_key] = value * sensor_config["scale"]

            for config_key, config_config in CONFIG_ENTITIES.items():
                value = await self.hass.async_add_executor_job(
                    self.modbus_client.read_register, config_config["address"]
                )
                if value is not None:
                    data[config_key] = value * config_config.get("scale", 1)

            return data
        except Exception as e:
            raise UpdateFailed(f"Erreur de mise à jour : {e}") from e