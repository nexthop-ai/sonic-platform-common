import typing
from sonic_platform_base.sonic_xcvr.api.public.cpo import CpoApi
from sonic_platform_base.sfp_base import SfpBase
from sonic_platform_base.sonic_xcvr.cpo_xcvr_api_factory import CpoXcvrApiFactory, DeviceEepromAccess, CpoHardwareId

class CpoSfpBase(SfpBase):
    def __init__(self, oe: SfpBase, elsfp: SfpBase, hardware_id: CpoHardwareId) -> None:
        SfpBase.__init__(self)
        self.oe = oe
        self.elsfp = elsfp
        self.hardware_id = hardware_id

        # Set up CPO API factory
        oe_access = DeviceEepromAccess(reader=self.oe.read_eeprom, writer=self.oe.write_eeprom)
        elsfp_access = DeviceEepromAccess(reader=self.elsfp.read_eeprom, writer=self.elsfp.write_eeprom)
        self._xcvr_api_factory = CpoXcvrApiFactory(oe_eeprom=oe_access, elsfp_eeprom=elsfp_access)

    def refresh_xcvr_api(self):
        oe_api, elsfp_api = self._xcvr_api_factory.create_xcvr_api(
            oe_bank=self.oe.bank,
            elsfp_bank=self.elsfp.bank,
            hardware_id=self.hardware_id,
        )
        self.oe.set_xcvr_api(oe_api)
        self.elsfp.set_xcvr_api(elsfp_api)

    # TODO: Implement CPO-specific methods here.

