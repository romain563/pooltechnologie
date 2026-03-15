"""Plateforme de nombres pour PoolTechnologie."""
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONFIG_ENTITIES

async def async_setup_entry(hass, entry, async_add_entities):
    """Configure les nombres PoolTechnologie."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    numbers = []

    for config_key, config_config in CONFIG_ENTITIES.items():
        if config_key in ["consigne_ph", "consigne_orp", "consigne_electrolyse", "concentration_correcteur_ph", "taille_bassin"]:
            numbers.append(PoolTechnologieNumber(coordinator, entry, config_key, config_config))

    async_add_entities(numbers, True)

class PoolTechnologieNumber(CoordinatorEntity, NumberEntity):
    """Représentation d'un nombre PoolTechnologie."""

    def __init__(self, coordinator, entry, config_key, config_config):
        """Initialise le nombre."""
        super().__init__(coordinator)
        self.entry = entry
        self.config_key = config_key
        self.config_config = config_config
        self._attr_name = f"{entry.data['name']} {config_config['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{config_config['unique_id']}"
        self._attr_icon = config_config["icon"]
        self._attr_native_unit_of_measurement = config_config.get("unit")
        self._attr_native_min_value = config_config.get("min", 0)
        self._attr_native_max_value = config_config.get("max", 1000)
        self._attr_native_step = config_config.get("step", 1)

    @property
    def available(self):
        """Retourne True si l'entité est disponible."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Retourne l'état du nombre."""
        if self.coordinator.data is not None:
            return round(self.coordinator.data.get(self.config_key), self.config_config["precision"])
        return None

    async def async_set_native_value(self, value):
        """Définit la valeur du nombre."""
        scaled_value = int(value / self.config_config.get("scale", 1))
        self.coordinator.modbus_client.write_register(self.config_config["address"], scaled_value)
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self):
        """Retourne les attributs d'état."""
        return {"modbus_address": self.config_config["address"]}
