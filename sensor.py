"""Plateforme de capteurs pour PoolTechnologie."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSORS

async def async_setup_entry(hass, entry, async_add_entities):
    """Configure les capteurs PoolTechnologie."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    sensors = []

    for sensor_key, sensor_config in SENSORS.items():
        sensors.append(PoolTechnologieSensor(coordinator, entry, sensor_key, sensor_config))

    async_add_entities(sensors, True)

class PoolTechnologieSensor(CoordinatorEntity, SensorEntity):
    """Représentation d'un capteur PoolTechnologie."""

    def __init__(self, coordinator, entry, sensor_key, sensor_config):
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
        self._attr_native_value = None

    @property
    def available(self):
        """Retourne True si l'entité est disponible."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Retourne l'état du capteur."""
        if self.coordinator.data is not None:
            return round(self.coordinator.data.get(self.sensor_key), self.sensor_config["precision"])
        return None

    @property
    def extra_state_attributes(self):
        """Retourne les attributs d'état."""
        return {"modbus_address": self.sensor_config["address"]}
