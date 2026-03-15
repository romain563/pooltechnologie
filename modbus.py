"""Communication Modbus pour PoolTechnologie."""
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import logging

_LOGGER = logging.getLogger(__name__)

class PoolTechnologieModbusClient:
    """Gère la communication Modbus pour PoolTechnologie."""

    def __init__(self, host, port, unit_id):
        """Initialise le client Modbus."""
        self.client = ModbusTcpClient(host, port=port, timeout=3)
        self.unit_id = unit_id

    def connect(self):
        """Se connecte à l'appareil Modbus."""
        if not self.client.connect():
            raise ConnectionError("Impossible de se connecter à l'électrolyseur PoolTechnologie.")

    def read_register(self, address, count=1):
        """Lit un registre depuis l'appareil Modbus."""
        try:
            response = self.client.read_holding_registers(address, count, slave=self.unit_id)
            if response.isError():
                raise ModbusException(response)
            return response.registers[0]
        except ModbusException as e:
            _LOGGER.error("Erreur de lecture Modbus : %s", e)
            return None

    def write_register(self, address, value):
        """Écrit une valeur dans un registre de l'appareil Modbus."""
        try:
            response = self.client.write_register(address, value, slave=self.unit_id)
            if response.isError():
                raise ModbusException(response)
            return True
        except ModbusException as e:
            _LOGGER.error("Erreur d'écriture Modbus : %s", e)
            return False

    def close(self):
        """Ferme la connexion Modbus."""
        self.client.close()
