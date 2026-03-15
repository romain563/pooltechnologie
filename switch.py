"""Plateforme d'interrupteurs pour PoolTechnologie."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONFIG_ENTITIES


async def async_setup_entry(hass, entry, async_add_entities):
    """Configure les interrupteurs PoolTechnologie."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    switches = []

    if "regulation_ph" in CONFIG_ENTITIES:
        switches.append(
            PoolTechnologieSwitch(
                coordinator, entry, "regulation_ph", CONFIG_ENTITIES["regulation_ph"]
            )
        )

    async_add_entities(switches, True)


class PoolTechnologieSwitch(CoordinatorEntity, SwitchEntity):
    """Représentation d'un interrupteur PoolTechnologie."""

    def __init__(self, coordinator, entry, config_key, config_config) -> None:
        """Initialise l'interrupteur."""
        super().__init__(coordinator)
        self.entry = entry
        self.config_key = config_key
        self.config_config = config_config
        self._attr_name = f"{entry.data['name']} {config_config['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{config_config['unique_id']}"
        self._attr_icon = "mdi:toggle-switch"

    @property
    def available(self) -> bool:
        """Retourne True si l'entité est disponible."""
        return self.coordinator.last_update_success

    @property
    def is_on(self) -> bool:
        """Retourne True si l'interrupteur est activé."""
        if self.coordinator.data is None:
            return False
        return bool(self.coordinator.data.get(self.config_key))

    async def async_turn_on(self, **kwargs) -> None:
        """Active l'interrupteur."""
        # CORRECTIF : write_register est synchrone → executor
        await self.hass.async_add_executor_job(
            self.coordinator.modbus_client.write_register,
            self.config_config["address"],
            1,
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Désactive l'interrupteur."""
        # CORRECTIF : write_register est synchrone → executor
        await self.hass.async_add_executor_job(
            self.coordinator.modbus_client.write_register,
            self.config_config["address"],
            0,
        )
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self) -> dict:
        """Retourne les attributs d'état."""
        return {"modbus_address": self.config_config["address"]}