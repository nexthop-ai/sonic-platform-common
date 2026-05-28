"""
    brcm_davisson_cpo_base.py

    Broadcom TH6 Davisson CPO ELSFP base.
"""

from sonic_platform_base.sonic_xcvr.cpo_optoe_base import OptoeJointModeElsfpBase
from sonic_platform_base.sonic_xcvr.mem_maps.public.cmis_pages.cmis_page_consts import (
    CMIS_EEPROM_PAGE_SIZE
)


class BrcmTh6ElsfpOptoeBase(OptoeJointModeElsfpBase):
    # The relocated ELSFP region begins at page 0xB0
    ELSFP_PAGE0_OFFSET = 0xB0 * CMIS_EEPROM_PAGE_SIZE
