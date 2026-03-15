"""Constantes pour l'intégration PoolTechnologie."""
from homeassistant.const import Platform

DOMAIN = "pooltechnologie"
DEFAULT_NAME = "PoolTechnologie"
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_IP = "192.168.0.100"
DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 1

CONF_REGULATION_ORP = "regulation_orp"

SENSORS = {
    "pH": {
        "name": "pH",
        "translation_key": "pH",
        "unique_id": "pH",
        "address": 259,
        "scale": 0.001,
        "precision": 2,
        "icon": "mdi:ph",
        "device_class": "ph",
    },
    "temperature_eau": {
        "name": "Température de l'eau",
        "translation_key": "temperature_eau",
        "unique_id": "temperature_eau",
        "address": 260,
        "unit": "°C",
        "scale": 0.1,
        "precision": 1,
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
    },
    "orp": {
        "name": "ORP",
        "translation_key": "orp",
        "unique_id": "orp",
        "address": 262,
        "unit": "mV",
        "scale": 1,
        "precision": 0,
        "icon": "mdi:lightning-bolt",
    },
    "taux_sel": {
        "name": "Salinité",
        "translation_key": "taux_sel",
        "unique_id": "taux_sel",
        "address": 261,
        "unit": "g/L",
        "scale": 0.1,
        "precision": 1,
        "icon": "mdi:shaker-outline",
    },
}
 
CONFIG_ENTITIES = {
    "consigne_ph": {
        "name": "Consigne pH",
        "translation_key": "consigne_ph",
        "unique_id": "consigne_ph",
        "address": 4207,
        "scale": 0.000390625,
        "precision": 1,
        "icon": "mdi:ph",
        "device_class": "ph",
        "min": 6.8,
        "max": 7.6,
        "step": 0.1,
    },
    "regulation_ph_auto": {
        "name": "Régulation pH automatique",
        "translation_key": "regulation_pH_auto",
        "unique_id": "regulation_pH_auto",
        "address": 4200,
    },
    "taille_bassin": {
        "name": "Volume du bassin",
        "translation_key": "taille_bassin",
        "unique_id": "taille_bassin",
        "address": 4111,
        "unit": "m³",
        "scale": 1,
        "precision": 0,
        "icon": "mdi:car-coolant-level",
        "device_class": "volume",
    },
    "consigne_orp": {
        "name": "Consigne ORP",
        "translation_key": "consigne_orp",
        "unique_id": "consigne_orp",
        "address": 4235,
        "unit": "mV",
        "scale": 1,
        "precision": 0,
        "icon": "mdi:cog",
        "min": 400,
        "max": 900,
        "step": 10,
    },
    "consigne_electrolyse": {
        "name": "Consigne électrolyse",
        "translation_key": "consigne_electrolyse",
        "unique_id": "consigne_electrolyse",
        "address": 4168,
        "unit": "%",
        "scale": 1,
        "precision": 0,
        "icon": "mdi:cog",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "concentration_correcteur_ph": {
        "name": "Concentration correcteur de pH",
        "translation_key": "concentration_correcteur_ph",
        "unique_id": "concentration_correcteur_ph",
        "address": 4208,
        "unit": "%",
        "scale": 1,
        "precision": 1,
        "icon": "mdi:flask-outline",
        "min": 5,
        "max": 50,
        "step": 1,
    },
}

PLATFORMS = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SWITCH,
    Platform.BINARY_SENSOR,
]
