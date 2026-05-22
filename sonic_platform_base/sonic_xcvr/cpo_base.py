from sonic_platform_base.sfp_base import SfpBase
from sonic_platform_base.sonic_xcvr.cpo_xcvr_api_factory import CpoXcvrApiFactory, DeviceEepromAccess, CpoHardwareId

class CpoSfpBase(SfpBase):
    def __init__(self, hardware_id: CpoHardwareId, oe_bank=0, elsfp_bank=0) -> None:
        self._thermal_list = []
        self._oe_bank = oe_bank
        self._elsfp_bank = elsfp_bank
        self._xcvr_api = None

        # Set up CPO xcvr API factory
        self.hardware_id = hardware_id
        oe_access = DeviceEepromAccess(reader=self.oe_read_eeprom, writer=self.oe_write_eeprom)
        elsfp_access = DeviceEepromAccess(reader=self.elsfp_read_eeprom, writer=self.elsfp_write_eeprom)
        self._xcvr_api_factory = CpoXcvrApiFactory(oe_access, elsfp_access)

    @property
    def bank(self):
        return self._oe_bank

    @property
    def oe_bank(self):
        return self._oe_bank

    @property
    def elsfp_bank(self):
        return self._elsfp_bank

    def oe_read_eeprom(self, offset, num_bytes):
        raise NotImplementedError

    def oe_write_eeprom(self, offset, num_bytes, write_buffer):
        raise NotImplementedError

    def elsfp_read_eeprom(self, offset, num_bytes):
        raise NotImplementedError

    def elsfp_write_eeprom(self, offset, num_bytes, write_buffer):
        raise NotImplementedError

    def refresh_xcvr_api(self):
        self._xcvr_api = self._xcvr_api_factory.create_xcvr_api(
            oe_bank=self._oe_bank,
            elsfp_bank=self._elsfp_bank,
            hardware_id=self.hardware_id,
        )

    # TODO: Implement CPO-specific methods below here.
