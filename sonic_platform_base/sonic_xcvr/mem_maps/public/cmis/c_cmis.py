"""
    c_cmis.py

    Implementation of XcvrMemMap for C-CMIS Rev 1.1
"""

from .cmis import CmisMemMap
from .pages import (
    CCmisModuleConfigSupportPage,
    CCmisMediaLaneConfigThresholdsPage,
    CCmisMediaLaneFlagsStatusPage,
    CCmisMediaLaneFecPmPage,
    CCmisMediaLaneLinkPmPage,
<<<<<<< HEAD
=======
    CCmisDataPathHostIfConfigPage,
    CCmisDataPathHostIfPmPage,
    CCmisDataPathHostIfFlagsPage,
    CCmisAlarmAdvertisementPage,
    CCmisHostLaneProvisioningAdvertisementPage,
    CCmisPmAdvertisementPage,
>>>>>>> 9322fc3 (NOS-11650: Updated C-CMIS FDD/FED memory maps and constants (#149))
)


class CCmisMemMap(CmisMemMap):
    def __init__(self, codes, bank=0):
        super(CCmisMemMap, self).__init__(codes, bank=bank)

        # C-CMIS-specific pages on top of the base CMIS memory map.
        self.add_pages(
<<<<<<< HEAD
            CCmisModuleConfigSupportPage(codes, bank=bank),  # 0x04
            CCmisMediaLaneFecPmPage(codes, bank=bank),       # 0x34
            CCmisMediaLaneLinkPmPage(codes, bank=bank),      # 0x35
=======
            CCmisModuleConfigSupportPage(codes, bank=bank),              # 0x04
            CCmisMediaLaneConfigThresholdsPage(codes, bank=bank),        # 0x30
            CCmisMediaLaneFlagsStatusPage(codes, bank=bank),             # 0x33
            CCmisMediaLaneFecPmPage(codes, bank=bank),                   # 0x34
            CCmisMediaLaneLinkPmPage(codes, bank=bank),                  # 0x35
            CCmisDataPathHostIfConfigPage(codes, bank=bank),             # 0x38
            CCmisDataPathHostIfPmPage(codes, bank=bank),                 # 0x3A
            CCmisDataPathHostIfFlagsPage(codes, bank=bank),              # 0x3B
            CCmisPmAdvertisementPage(codes, bank=bank),      # 0x42
            CCmisAlarmAdvertisementPage(codes, bank=bank),               # 0x44
            CCmisHostLaneProvisioningAdvertisementPage(codes, bank=bank),  # 0x45
>>>>>>> 9322fc3 (NOS-11650: Updated C-CMIS FDD/FED memory maps and constants (#149))
        )
