"""Plateforme de capteurs pour PoolTechnologie."""
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSORS


async def async_setup_entry(hass, entry, async_add_entities):
    """Configure les capteurs PoolTechnologie."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    sensors = [
        PoolTechnologieSensor(coordinator, entry, sensor_key, sensor_config)
        for sensor_key, sensor_config in SENSORS.items()
    ]
    async_add_entities(sensors, True)


class PoolTechnologieSensor(CoordinatorEntity, SensorEntity):
    """Représentation d'un capteur PoolTechnologie."""

    def __init__(self, coordinator, entry, sensor_key, sensor_config) -> None:
        """Initialise le capteur."""
        super().__init__(coordinator)
        self.entry = entry
        self.sensor_key = sensor_key
        self.sensor_config = sensor_config
        self._attr_name = f"{entry.data['name']} {sensor_config['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_config['unique_id']}"
        self._attr_icon = sensor_config["icon"]
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        # CORRECTIF : active l'historique long terme dans HA (statistiques, graphiques)
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def available(self) -> bool:
        """Retourne True si l'entité est disponible."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Retourne l'état du capteur."""
        if self.coordinator.data is None:
            return None
        # CORRECTIF : guard explicite avant round() — évite TypeError si la clé est absente
        value = self.coordinator.data.get(self.sensor_key)
        if value is None:
            return None
        return round(value, self.sensor_config["precision"])

    @property
    def extra_state_attributes(self) -> dict:
        """Retourne les attributs d'état."""
        return {"modbus_address": self.sensor_config["address"]}