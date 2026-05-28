from sonic_platform_base.sonic_xcvr.eeprom_rw import EepromReadWriteMixin
from sonic_platform_base.sonic_xcvr.cpo_api_factory import OeApiFactory, ElsfpApiFactory, CpoHardwareId
from sonic_platform_base.sonic_xcvr.mem_maps.public.cmis_pages.cmis_page_consts import (
    CMIS_ARCH_PAGES,
    CMIS_EEPROM_PAGE_SIZE
)


class OeBase(EepromReadWriteMixin):
    def __init__(self, hardware_id: CpoHardwareId, bank: int = 0):
        self.bank = bank
        self._oe_api = None
        self.hardware_id = hardware_id
        self._oe_api_factory = OeApiFactory(self)

    def refresh_oe_api(self):
        self._oe_api = self._oe_api_factory.create_oe_api()

    def get_oe_api(self):
        if self._oe_api is None:
            self.refresh_oe_api()
        return self._oe_api

    # TODO: Implement OE-specific methods


class ElsfpBase(EepromReadWriteMixin):
    def __init__(self, hardware_id: CpoHardwareId = None, bank: int = 0):
        self.bank = bank
        self._elsfp_api = None
        self.hardware_id = hardware_id
        self._elsfp_api_factory = ElsfpApiFactory(self)

    def refresh_elsfp_api(self):
        self._elsfp_api = self._elsfp_api_factory.create_elsfp_api()

    def get_elsfp_api(self):
        if self._elsfp_api is None:
            self.refresh_elsfp_api()
        return self._elsfp_api

    # TODO: Implement ELSFP-specific methods


class JointModeElsfpBase(ElsfpBase):
    """ELSFP base for devices that operate in "joint mode", where the ELSFP
    region is relocated within a shared (e.g. CMIS MCU) address space.

    The ELSFP MemMap emits offsets in its own view starting at page 0. On these
    devices that view must be shifted to start at ``ELSFP_PAGE0_OFFSET`` within
    the underlying linear address space. The page-0 offset is the only
    thing that varies between vendors -- subclasses set ``ELSFP_PAGE0_OFFSET``
    and everything else (translation + EEPROM access) is handled here.
    """

    # Offset of the relocated ELSFP page 0 within the underlying address space.
    # Vendor subclasses must override this.
    ELSFP_PAGE0_OFFSET = None
    BANK_STRIDE = CMIS_ARCH_PAGES * CMIS_EEPROM_PAGE_SIZE

    def _translate(self, offset):
        bank, bank_relative_offset = divmod(offset, self.BANK_STRIDE)
        return bank * self.BANK_STRIDE + self.ELSFP_PAGE0_OFFSET + bank_relative_offset

    def read_eeprom(self, offset, num_bytes):
        return super().read_eeprom(self._translate(offset), num_bytes)

    def write_eeprom(self, offset, num_bytes, write_buffer):
        return super().write_eeprom(self._translate(offset), num_bytes, write_buffer)


class CpoBase:
    def __init__(self, hardware_id: CpoHardwareId, oe: OeBase, elsfp: ElsfpBase):
        self.hardware_id = hardware_id
        self.oe = oe
        self.elsfp = elsfp

# TODO: Implement CPO-specific methods
#     def do_fiber_check(self, lane):
#         oe_api = self.oe.get_oe_api()
#         oe_api.do_fiber_check(lane)
#
#     def tx_disable(self, lane):
#         elsp_api = self.elsfp.get_elsp_api()
#         elsp_api.tx_disable(lane)
