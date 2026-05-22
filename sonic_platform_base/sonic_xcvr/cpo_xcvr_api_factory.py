"""
    cpo_xcvr_api_factory.py

    Factory class responsible for instantiating the appropriate XcvrApi
    implementation for a CPO SFP in SONiC
"""

from dataclasses import dataclass
from typing import Callable, Optional

from sonic_platform_base.sonic_xcvr.xcvr_eeprom import XcvrEeprom
from sonic_platform_base.sonic_xcvr.api.public.cpo import CpoApi
from sonic_platform_base.sonic_xcvr.codes.public.cmis import CmisCodes
from sonic_platform_base.sonic_xcvr.api.public.cmis import CmisApi
from sonic_platform_base.sonic_xcvr.mem_maps.public.cmis import CmisMemMap
from sonic_platform_base.sonic_xcvr.api.public.elsfp import ElsfpApi
from sonic_platform_base.sonic_xcvr.mem_maps.public.elsfp import ElsfpMemMap


@dataclass
class CpoHardwareId:
    oe_id: str
    elsfp_id: Optional[str]


@dataclass
class DeviceEepromAccess:
    reader: Callable[[int, int], Optional[bytearray]]
    writer: Callable[[int, int, bytearray], bool]


class CpoXcvrApiFactory():
    def __init__(self, oe_eeprom: DeviceEepromAccess, elsfp_eeprom: DeviceEepromAccess):
        self.oe_eeprom = oe_eeprom
        self.elsfp_eeprom = elsfp_eeprom

    def _create_api(self, codes_class, mem_map_class, api_class, reader, writer, bank=0):
        mem_map = mem_map_class(codes_class, bank=bank)
        xcvr_eeprom = XcvrEeprom(reader, writer, mem_map)
        return api_class(xcvr_eeprom)

    def create_oe_api(self, hardware_id: CpoHardwareId, bank=0):
        if hardware_id.oe_id == "EXAMPLE":
            # TODO: How can we handle memory maps,
            # codes and APIs that are intentionally not upstreamed
            # in this approach?
            return self._create_api(
                codes_class=CmisCodes,
                mem_map_class=CmisMemMap,
                api_class=CmisApi,
                reader=self.oe_eeprom.reader,
                writer=self.oe_eeprom.writer,
                bank=bank
            )

        raise ValueError(f"Could not determine what OE API to use for OE ID: {hardware_id.oe_id}")

    def get_elsfp_vendor_info(self, hardware_id: CpoHardwareId):
        return None

    def create_elsfp_api(self, hardware_id: CpoHardwareId, bank=0):
        if hardware_id.elsfp_id:
            # ELSFP ID has been passed, meaning the platform probably does not have
            # pluggable laser sources. Pick the ELSFP memory map based on the ELSFP
            # and OE IDs.
            if hardware_id.oe_id == "EXAMPLE" and hardware_id.elsfp_id == "EXAMPLE":
                return self._create_api(
                    codes_class=CmisCodes,
                    mem_map_class=ElsfpMemMap,
                    api_class=ElsfpApi,
                    reader=self.elsfp_eeprom.reader,
                    writer=self.elsfp_eeprom.writer,
                    bank=bank
                )

        # Handle platforms with pluggable ELSFP modules. We will need to
        # dynamically identify what Xcvr API to use for the ELSFP by
        # reading the EEPROM of the currently plugged in ELSFP.
        # Then, we would pick the ELSFP memory map / API based on the vendor information
        # and OE ID.
        elsfp_vendor_info = self.get_elsfp_vendor_info(hardware_id=hardware_id)
        if hardware_id.oe_id == "EXAMPLE":
            return self._create_api(
                codes_class=CmisCodes,
                mem_map_class=ElsfpMemMap,
                api_class=ElsfpApi,
                reader=self.elsfp_eeprom.reader,
                writer=self.elsfp_eeprom.writer,
                bank=bank
            )

        raise ValueError(f"Could not determine what ELSFP API to use for OE ID {hardware_id.oe_id} and ELSFP ID {hardware_id.elsfp_id}")

    def create_xcvr_api(self, oe_bank: int, elsfp_bank: int, hardware_id: CpoHardwareId):
        oe = self.create_oe_api(bank=oe_bank, hardware_id=hardware_id)
        elsfp = self.create_elsfp_api(bank=elsfp_bank, hardware_id=hardware_id)

        return CpoApi(
            optical_engine_xcvr_api=oe,
            external_laser_source_xcvr_api=elsfp
        )
