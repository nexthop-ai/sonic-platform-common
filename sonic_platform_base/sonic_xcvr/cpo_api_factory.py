from typing import Optional
from enum import Enum
from dataclasses import dataclass

from sonic_platform_base.sonic_xcvr.xcvr_eeprom import XcvrEeprom
from sonic_platform_base.sonic_xcvr.codes.public.cmis import CmisCodes
from sonic_platform_base.sonic_xcvr.api.public.cmis import CmisApi
from sonic_platform_base.sonic_xcvr.mem_maps.broadcom.th6_oe import BroadcomTh6OpticalEngineMemMap
from sonic_platform_base.sonic_xcvr.api.broadcom.th6_oe import BroadcomTh6OeApi
from sonic_platform_base.sonic_xcvr.mem_maps.broadcom.th6_elsfp import BroadcomTh6ElsfpMemMap
from sonic_platform_base.sonic_xcvr.api.broadcom.th6_elsfp import BroadcomTh6ElsfpApi


class OeId(Enum):
    NVIDIA_SP6 = 1
    BROADCOM_DAVISSON = 2


class ElsfpId(Enum):
    EXAMPLE = 1


@dataclass
class CpoHardwareId:
    oe_id: OeId
    elsfp_id: Optional[ElsfpId]


class OeApiFactory:
    def __init__(self, oe: "OeBase"):
        self._oe = oe

    def _create_api(self, codes_class, mem_map_class, api_class):
        mem_map = mem_map_class(codes_class, self._oe.bank)
        oe_eeprom = XcvrEeprom(self._oe.read_eeprom, self._oe.write_eeprom, mem_map)
        return api_class(oe_eeprom)

    def create_oe_api(self):
        if self._oe.hardware_id.oe_id == OeId.NVIDIA_SP6:
            # Create NVIDIA API
            pass

        if self._oe.hardware_id.oe_id == OeId.BROADCOM_DAVISSON:
            return self._create_api(
                codes_class=CmisCodes,
                mem_map_class=BroadcomTh6OpticalEngineMemMap,
                api_class=BroadcomTh6OeApi
            )

        raise ValueError(f"Could not determine what OE API to use for OE ID: {self._oe.hardware_id.oe_id}")


class ElsfpApiFactory:
    def __init__(self, elsfp: "ElsfpBase"):
        self._elsfp = elsfp

    def _create_api(self, codes_class, mem_map_class, api_class):
        mem_map = mem_map_class(codes_class, self._elsfp.bank)
        elsfp_eeprom = XcvrEeprom(self._elsfp.read_eeprom, self._elsfp.write_eeprom, mem_map)
        return api_class(elsfp_eeprom)

    def create_elsfp_api(self):
        if self._elsfp.hardware_id.elsfp_id is None:
            # read vendor name or part number from EEPROM
            # and determine the correct memory map to use
            # based on that information.
            if self._elsfp.hardware_id.oe_id == OeId.BROADCOM_DAVISSON:
                return self._create_api(
                    codes_class=CmisCodes,
                    mem_map_class=BroadcomTh6ElsfpMemMap,
                    api_class=BroadcomTh6ElsfpApi
                )
        elif self._elsfp.hardware_id.elsfp_id == ElsfpId.EXAMPLE:
            # ELSFP ID is set -- use whatever API is
            # appropriate for that ID.
            pass

        raise ValueError(
            f"Could not determine what ELSFP API to use for CPO HW ID. "
            f"OE ID: {self._elsfp.hardware_id.oe_id}, ELSFP ID: {self._elsfp.hardware_id.elsfp_id}"
        )
