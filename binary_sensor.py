"""Plateforme de capteurs binaires pour PoolTechnologie."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Configure les capteurs binaires PoolTechnologie."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([PoolTechnologieConnectionSensor(coordinator, entry)], True)

class PoolTechnologieConnectionSensor(CoordinatorEntity, BinarySensorEntity):
    """Représentation d'un capteur binaire de connexion PoolTechnologie."""

    def __init__(self, coordinator, entry):
        """Initialise le capteur de connexion."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_name = f"{entry.data['name']} Connexion Modbus"
        self._attr_unique_id = f"{entry.entry_id}_connection"
        self._attr_icon = "mdi:lan-connect"

    @property
    def available(self):
        """Retourne True si l'entité est disponible."""
        return True

    @property
    def is_on(self):
        """Retourne True si l'appareil est connecté."""
        return self.coordinator.last_update_success
