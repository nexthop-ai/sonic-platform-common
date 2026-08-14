"""
    page30.py

    C-CMIS Page 30h - Media Lane Configurable Thresholds.
"""

from .page import CmisPage
from .....fields.xcvr_field import NumberRegField, RegBitField
from .....fields import consts


class CCmisMediaLaneConfigThresholdsPage(CmisPage):
    """C-CMIS Page 30h: media-lane configurable Rx power / degrade thresholds."""

    def __init__(self, codes, bank=0, page=0x30):
        super().__init__(codes, page=page, bank=bank)

        self.fields[consts.MEDIA_LANE_CONFIG_THRESHOLDS] = [
            NumberRegField(consts.TOTAL_PWR_HIGH_ALARM_THRESH, self.getaddr(128), format=">h", size=2, scale=100.0),
            NumberRegField(consts.TOTAL_PWR_LOW_ALARM_THRESH, self.getaddr(130), format=">h", size=2, scale=100.0),
            NumberRegField(consts.TOTAL_PWR_HIGH_WARN_THRESH, self.getaddr(132), format=">h", size=2, scale=100.0),
            NumberRegField(consts.TOTAL_PWR_LOW_WARN_THRESH, self.getaddr(134), format=">h", size=2, scale=100.0),
            NumberRegField(consts.SIG_PWR_HIGH_ALARM_THRESH, self.getaddr(136), format=">h", size=2, scale=100.0),
            NumberRegField(consts.SIG_PWR_LOW_ALARM_THRESH, self.getaddr(138), format=">h", size=2, scale=100.0),
            NumberRegField(consts.SIG_PWR_HIGH_WARN_THRESH, self.getaddr(140), format=">h", size=2, scale=100.0),
            NumberRegField(consts.SIG_PWR_LOW_WARN_THRESH, self.getaddr(142), format=">h", size=2, scale=100.0),
            NumberRegField(consts.TOTAL_PWR_USE_CFG_THRESH, self.getaddr(144), RegBitField("Bit1", 1)),
            NumberRegField(consts.SIG_PWR_USE_CFG_THRESH, self.getaddr(144), RegBitField("Bit0", 0)),
            NumberRegField(consts.FDD_RAISE_THRESH, self.getaddr(160), format=">H", size=2, ro=False),
            NumberRegField(consts.FDD_CLEAR_THRESH, self.getaddr(162), format=">H", size=2, ro=False),
            NumberRegField(consts.FED_RAISE_THRESH, self.getaddr(164), format=">H", size=2, ro=False),
            NumberRegField(consts.FED_CLEAR_THRESH, self.getaddr(166), format=">H", size=2, ro=False),
            NumberRegField(consts.MEDIA_FDD_FED_ENABLE, self.getaddr(168),
                RegBitField(consts.FED_ENABLE, 1, ro=False),
                RegBitField(consts.FDD_ENABLE, 0, ro=False),
                ro=False),
        ]
