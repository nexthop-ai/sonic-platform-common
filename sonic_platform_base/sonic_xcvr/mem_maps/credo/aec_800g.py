"""
    aec_800g.py

    Implementation of Credo AEC cable specific XcvrMemMap for CMIS Rev 5.0
"""

from ..public.cmisTargetFWUpgrade import CmisTargetFWUpgradeMemMap
from ...fields.xcvr_field import (
    NumberRegField,
    RegGroupField,
)
from ...fields import consts

class CmisAec800gMemMap(CmisTargetFWUpgradeMemMap):
    def __init__(self, codes, bank=0):
        super().__init__(codes, bank=bank)

        self.VENDOR_CUSTOM = RegGroupField(consts.VENDOR_CUSTOM,
            NumberRegField(consts.TARGET_MODE, self.getaddr(0x0, 64), ro=False)
        )
