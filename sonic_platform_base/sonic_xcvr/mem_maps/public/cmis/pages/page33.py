"""
    page33.py

    C-CMIS Page 33h - Media Lane Flags and Status.
"""

from .page import CmisPage
from .....fields.xcvr_field import NumberRegField, RegBitField
from .....fields import consts


class CCmisMediaLaneFlagsStatusPage(CmisPage):
    """C-CMIS Page 33h: latched media-lane alarms and media-lane status."""

    def __init__(self, codes, bank=0, page=0x33):
        super().__init__(codes, page=page, bank=bank)

        self.fields[consts.MEDIA_LANE_FLAGS_STATUS] = [
            NumberRegField(consts.L_TX_LOA, self.getaddr(128), RegBitField("Bit5", 5)),
            NumberRegField(consts.L_TX_OOA, self.getaddr(128), RegBitField("Bit4", 4)),
            NumberRegField(consts.L_TX_LOL_CMU, self.getaddr(128), RegBitField("Bit3", 3)),
            NumberRegField(consts.L_TX_LOL_REF_CLK, self.getaddr(128), RegBitField("Bit2", 2)),
            NumberRegField(consts.L_TX_LOL_DESKEW, self.getaddr(128), RegBitField("Bit1", 1)),
            NumberRegField(consts.L_TX_FIFO, self.getaddr(128), RegBitField("Bit0", 0)),
            NumberRegField(consts.L_RX_LOF, self.getaddr(130), RegBitField("Bit7", 7)),
            NumberRegField(consts.L_RX_LOM, self.getaddr(130), RegBitField("Bit6", 6)),
            NumberRegField(consts.L_RX_LOL_DEMOD, self.getaddr(130), RegBitField("Bit5", 5)),
            NumberRegField(consts.L_RX_LOL_CD, self.getaddr(130), RegBitField("Bit4", 4)),
            NumberRegField(consts.L_RX_LOA, self.getaddr(130), RegBitField("Bit3", 3)),
            NumberRegField(consts.L_RX_OOA, self.getaddr(130), RegBitField("Bit2", 2)),
            NumberRegField(consts.L_RX_LOL_DESKEW, self.getaddr(130), RegBitField("Bit1", 1)),
            NumberRegField(consts.L_RX_LOL_FIFO, self.getaddr(130), RegBitField("Bit0", 0)),
            NumberRegField(consts.MEDIA_FDD_FED_FLAGS, self.getaddr(132),
                RegBitField(consts.L_RX_FED_PM, 1),
                RegBitField(consts.L_RX_FDD_PM, 0),
                bitdecode=True),
            NumberRegField(consts.L_RX_STAT_MNT_AIS, self.getaddr(133), RegBitField("Bit5", 5)),
            NumberRegField(consts.L_RX_STAT_MNT_LCK, self.getaddr(133), RegBitField("Bit4", 4)),
            NumberRegField(consts.L_RX_PYLD_TYP_MM, self.getaddr(133), RegBitField("Bit3", 3)),
            NumberRegField(consts.L_RD, self.getaddr(133), RegBitField("Bit2", 2)),
            NumberRegField(consts.L_LD, self.getaddr(133), RegBitField("Bit1", 1)),
            NumberRegField(consts.L_STAT_RF, self.getaddr(133), RegBitField("Bit0", 0)),
            NumberRegField(consts.RX_PYLD_TYPE, self.getaddr(188), format=">B", size=1),
        ]
