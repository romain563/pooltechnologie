"""Plateforme de nombres pour PoolTechnologie."""
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONFIG_ENTITIES, CONF_REGULATION_ORP

# Entités toujours présentes
_NUMBER_KEYS_BASE = {
    "consigne_ph",
    "consigne_electrolyse",
    "concentration_correcteur_ph",
    "taille_bassin",
}

# Entités conditionnelles — uniquement si régulation ORP activée
_NUMBER_KEYS_ORP = {
    "consigne_orp",
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Configure les nombres PoolTechnologie."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    regulation_orp = entry.options.get(CONF_REGULATION_ORP, entry.data.get(CONF_REGULATION_ORP, False))
    active_keys = _NUMBER_KEYS_BASE | (_NUMBER_KEYS_ORP if regulation_orp else set())

    numbers = [
        PoolTechnologieNumber(coordinator, entry, config_key, config_config)
        for config_key, config_config in CONFIG_ENTITIES.items()
        if config_key in active_keys
    ]
    async_add_entities(numbers, True)


class PoolTechnologieNumber(CoordinatorEntity, NumberEntity):
    """Représentation d'un nombre PoolTechnologie."""

    def __init__(self, coordinator, entry, config_key, config_config) -> None:
        """Initialise le nombre."""
        super().__init__(coordinator)
        self.entry = entry
        self.config_key = config_key
        self.config_config = config_config
        self._attr_name = f"{entry.data['name']} {config_config['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{config_config['unique_id']}"
        self._attr_icon = config_config.get("icon", "mdi:cog")
        self._attr_native_unit_of_measurement = config_config.get("unit")
        self._attr_native_min_value = config_config.get("min", 0)
        self._attr_native_max_value = config_config.get("max", 1000)
        self._attr_native_step = config_config.get("step", 1)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Pool Technologie",
        )

    @property
    def available(self) -> bool:
        """Retourne True si l'entité est disponible."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Retourne l'état du nombre."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.config_key)
        if value is None:
            return None
        return round(value, self.config_config.get("precision", 1))

    async def async_set_native_value(self, value: float) -> None:
        """Définit la valeur du nombre."""
        scaled_value = int(value / self.config_config.get("scale", 1))
        await self.hass.async_add_executor_job(
            self.coordinator.modbus_client.write_register,
            self.config_config["address"],
            scaled_value,
        )
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self) -> dict:
        """Retourne les attributs d'état."""
        return {"modbus_address": self.config_config["address"]}