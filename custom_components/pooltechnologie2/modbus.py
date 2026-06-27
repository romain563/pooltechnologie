"""Communication Modbus pour PoolTechnologie."""
from pymodbus.client import ModbusTcpClient
from pymodbus import ModbusException
import logging

_LOGGER = logging.getLogger(__name__)


class PoolTechnologieModbusClient:
    """Gère la communication Modbus pour PoolTechnologie."""

    def __init__(self, host: str, port: int, unit_id: int) -> None:
        """Initialise le client Modbus."""
        self._host = host
        self._port = port
        self.unit_id = unit_id
        self.client = ModbusTcpClient(host, port=port)

    def connect(self) -> None:
        """Se connecte à l'appareil Modbus."""
        if not self.client.connect():
            raise ConnectionError("Impossible de se connecter à l'électrolyseur PoolTechnologie.")

    def read_register(self, address: int, count: int = 1):
        """Lit un registre depuis l'appareil Modbus.

        Retourne None si l'adresse est invalide (erreur Modbus normale).
        Lève ConnectionError si l'appareil est injoignable (connexion perdue).
        """
        # Reconnexion automatique si la connexion a été fermée par pymodbus
        if not self.client.connected:
            _LOGGER.debug("Connexion perdue, tentative de reconnexion...")
            if not self.client.connect():
                raise ConnectionError("Appareil injoignable.")

        try:
            response = self.client.read_holding_registers(
                address, count=count, device_id=self.unit_id
            )
        except ModbusException as e:
            # Connexion coupée pendant la lecture → on ferme proprement
            # et on lève ConnectionError pour que le coordinateur passe
            # last_update_success à False
            self.client.close()
            raise ConnectionError(f"Connexion perdue lors de la lecture (adresse {address}) : {e}") from e

        if response.isError():
            # Erreur Modbus normale (adresse invalide, etc.) → on logue en debug
            # seulement pour ne pas polluer les logs quand l'appareil est éteint
            _LOGGER.debug("Réponse d'erreur Modbus (adresse %s) : %s", address, response)
            return None

        return response.registers[0]

    def write_register(self, address: int, value: int) -> bool:
        """Écrit un registre depuis l'appareil Modbus."""
        if not self.client.connected:
            _LOGGER.debug("Connexion perdue, tentative de reconnexion...")
            if not self.client.connect():
                raise ConnectionError("Appareil injoignable.")

        try:
            response = self.client.write_register(
                address, value=value, device_id=self.unit_id
            )
        except ModbusException as e:
            self.client.close()
            raise ConnectionError(f"Connexion perdue lors de l'écriture (adresse {address}) : {e}") from e

        if response.isError():
            _LOGGER.error("Réponse d'erreur Modbus (adresse %s) : %s", address, response)
            return False

        return True

    def close(self) -> None:
        """Ferme la connexion Modbus."""
        self.client.close()