"""Plateforme de capteurs binaires pour PoolTechnologie."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Configure les capteurs binaires PoolTechnologie."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([PoolTechnologieConnectionSensor(coordinator, entry)], True)


class PoolTechnologieConnectionSensor(CoordinatorEntity, BinarySensorEntity):
    """Représentation d'un capteur binaire de connexion PoolTechnologie."""

    def __init__(self, coordinator, entry) -> None:
        """Initialise le capteur de connexion."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_name = f"{entry.data['name']} Connexion Modbus"
        self._attr_unique_id = f"{entry.entry_id}_connection"
        self._attr_icon = "mdi:lan-connect"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["name"],
            manufacturer="Pool Technologie",
        )

    @property
    def available(self) -> bool:
        """Indisponible si le coordinateur n'arrive plus à joindre l'appareil."""
        return self.coordinator.last_update_success

    @property
    def is_on(self) -> bool:
        """Retourne True si la connexion Modbus est active."""
        return self.coordinator.last_update_success