"""Communication Modbus pour PoolTechnologie."""
from pymodbus.client import ModbusTcpClient
# Import stable depuis pymodbus 3.x — ne pas utiliser pymodbus.exceptions directement
from pymodbus import ModbusException
from pymodbus.exceptions import ConnectionException
import logging

_LOGGER = logging.getLogger(__name__)


class PoolTechnologieModbusClient:
    """Gère la communication Modbus pour PoolTechnologie."""

    def __init__(self, host: str, port: int, unit_id: int) -> None:
        """Initialise le client Modbus."""
        # En pymodbus 3.11+, tous les paramètres après host sont keyword-only
        self.client = ModbusTcpClient(host, port=port)
        self.unit_id = unit_id

    def connect(self) -> None:
        """Se connecte à l'appareil Modbus."""
        if not self.client.connect():
            raise ConnectionError("Impossible de se connecter à l'électrolyseur PoolTechnologie.")

    def read_register(self, address: int, count: int = 1):
        """Lit un registre depuis l'appareil Modbus."""
        try:
            # pymodbus 3.11+ : address seul est positionnel, count et device_id sont keyword-only
            response = self.client.read_holding_registers(address, count=count, device_id=self.unit_id)
        except ModbusException as e:
            # Exception interne pymodbus (timeout, connexion perdue, etc.)
            _LOGGER.error("Erreur de communication Modbus (adresse %s) : %s", address, e)
            return None

        # Réponse d'erreur Modbus retournée par l'appareil (adresse invalide, etc.)
        if response.isError():
            _LOGGER.error("Réponse d'erreur Modbus (adresse %s) : %s", address, response)
            return None

        return response.registers[0]

    def write_register(self, address: int, value: int) -> bool:
        """Écrit une valeur dans un registre de l'appareil Modbus."""
        try:
            # pymodbus 3.11+ : address seul est positionnel, value et device_id sont keyword-only
            response = self.client.write_register(address, value=value, device_id=self.unit_id)
        except ModbusException as e:
            _LOGGER.error("Erreur de communication Modbus (adresse %s) : %s", address, e)
            return False

        if response.isError():
            _LOGGER.error("Réponse d'erreur Modbus (adresse %s) : %s", address, response)
            return False

        return True

    def close(self) -> None:
        """Ferme la connexion Modbus."""
        self.client.close()