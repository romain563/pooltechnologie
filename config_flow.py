"""Flux de configuration pour l'intégration PoolTechnologie."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_IP, DEFAULT_PORT, DEFAULT_UNIT_ID, DEFAULT_SCAN_INTERVAL, CONF_REGULATION_ORP

class PoolTechnologieConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gère le flux de configuration pour PoolTechnologie."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Gère l'étape initiale de configuration."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("name", default=DEFAULT_NAME): str,
            vol.Required("ip", default=DEFAULT_IP): str,
            vol.Required("port", default=DEFAULT_PORT): int,
            vol.Required("unit_id", default=DEFAULT_UNIT_ID): int,
            vol.Required("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
            vol.Required(CONF_REGULATION_ORP, default=False): bool,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Récupère le flux d'options pour ce gestionnaire."""
        return PoolTechnologieOptionsFlow(config_entry)

class PoolTechnologieOptionsFlow(config_entries.OptionsFlow):
    """Gère le flux d'options pour PoolTechnologie."""

    def __init__(self, config_entry):
        """Initialise le flux d'options."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Gère les options de configuration."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Required(CONF_REGULATION_ORP, default=self.config_entry.options.get(CONF_REGULATION_ORP, False)): bool,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
