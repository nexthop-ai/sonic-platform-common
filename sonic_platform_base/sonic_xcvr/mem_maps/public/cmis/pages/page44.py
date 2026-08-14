"""
    page44.py

    C-CMIS Page 44h - Alarm and Status Advertisement.
"""

from .page import CmisPage
from .....fields.xcvr_field import NumberRegField, RegBitField
from .....fields import consts


class CCmisAlarmAdvertisementPage(CmisPage):
    """C-CMIS Page 44h: advertises which media/host alarms and status are implemented."""

    def __init__(self, codes, bank=0, page=0x44):
        super().__init__(codes, page=page, bank=bank)

        self.fields[consts.ALARM_ADVERTISEMENT] = [
            NumberRegField(consts.MEDIA_TX_LOA_IMPL, self.getaddr(128), RegBitField("Bit5", 5)),
            NumberRegField(consts.MEDIA_TX_OOA_IMPL, self.getaddr(128), RegBitField("Bit4", 4)),
            NumberRegField(consts.MEDIA_TX_LOL_CMU_IMPL, self.getaddr(128), RegBitField("Bit3", 3)),
            NumberRegField(consts.MEDIA_TX_LOL_REF_CLK_IMPL, self.getaddr(128), RegBitField("Bit2", 2)),
            NumberRegField(consts.MEDIA_TX_LOL_DESKEW_IMPL, self.getaddr(128), RegBitField("Bit1", 1)),
            NumberRegField(consts.MEDIA_TX_FIFO_IMPL, self.getaddr(128), RegBitField("Bit0", 0)),
            NumberRegField(consts.MEDIA_RX_LOF_IMPL, self.getaddr(129), RegBitField("Bit7", 7)),
            NumberRegField(consts.MEDIA_RX_LOM_IMPL, self.getaddr(129), RegBitField("Bit6", 6)),
            NumberRegField(consts.MEDIA_RX_LOL_DEMOD_IMPL, self.getaddr(129), RegBitField("Bit5", 5)),
            NumberRegField(consts.MEDIA_RX_LOL_CD_IMPL, self.getaddr(129), RegBitField("Bit4", 4)),
            NumberRegField(consts.MEDIA_RX_LOA_IMPL, self.getaddr(129), RegBitField("Bit3", 3)),
            NumberRegField(consts.MEDIA_RX_OOA_IMPL, self.getaddr(129), RegBitField("Bit2", 2)),
            NumberRegField(consts.MEDIA_RX_LOL_DESKEW_IMPL, self.getaddr(129), RegBitField("Bit1", 1)),
            NumberRegField(consts.MEDIA_RX_LOL_FIFO_IMPL, self.getaddr(129), RegBitField("Bit0", 0)),
            NumberRegField(consts.MEDIA_RX_FED_ALM_IMPL, self.getaddr(130), RegBitField("Bit1", 1)),
            NumberRegField(consts.MEDIA_RX_FDD_ALM_IMPL, self.getaddr(130), RegBitField("Bit0", 0)),
            NumberRegField(consts.RX_STAT_MNT_AIS_IMPL, self.getaddr(131), RegBitField("Bit5", 5)),
            NumberRegField(consts.RX_STAT_MNT_LCK_IMPL, self.getaddr(131), RegBitField("Bit4", 4)),
            NumberRegField(consts.MEDIA_RX_PYLD_TYP_MM_IMPL, self.getaddr(131), RegBitField("Bit3", 3)),
            NumberRegField(consts.MEDIA_RD_IMPL, self.getaddr(131), RegBitField("Bit2", 2)),
            NumberRegField(consts.MEDIA_LD_IMPL, self.getaddr(131), RegBitField("Bit1", 1)),
            NumberRegField(consts.MEDIA_STAT_RF_IMPL, self.getaddr(131), RegBitField("Bit0", 0)),
            NumberRegField(consts.HOST_TX_FED_ALM_IMPL, self.getaddr(132), RegBitField("Bit1", 1)),
            NumberRegField(consts.HOST_TX_FDD_ALM_IMPL, self.getaddr(132), RegBitField("Bit0", 0)),
            NumberRegField(consts.HOST_RX_RD_IMPL, self.getaddr(133), RegBitField("Bit4", 4)),
            NumberRegField(consts.HOST_RX_LD_IMPL, self.getaddr(133), RegBitField("Bit3", 3)),
            NumberRegField(consts.HOST_RX_CSTAT_MNT_LCK_IMPL, self.getaddr(133), RegBitField("Bit2", 2)),
            NumberRegField(consts.HOST_TX_RD_IMPL, self.getaddr(133), RegBitField("Bit1", 1)),
            NumberRegField(consts.HOST_TX_LD_IMPL, self.getaddr(133), RegBitField("Bit0", 0)),
            NumberRegField(consts.HOST_RX_FLEXE_RPF_IMPL, self.getaddr(134), RegBitField("Bit7", 7)),
            NumberRegField(consts.HOST_RX_FLEXE_GID_MM_IMPL, self.getaddr(134), RegBitField("Bit6", 6)),
            NumberRegField(consts.HOST_RX_FLEXE_INSTANCE_MAP_MM_IMPL, self.getaddr(134), RegBitField("Bit5", 5)),
            NumberRegField(consts.HOST_RX_FLEXE_CALENDAR_MM_IMPL, self.getaddr(134), RegBitField("Bit4", 4)),
            NumberRegField(consts.HOST_RX_FLEXE_IID_MM_IMPL, self.getaddr(134), RegBitField("Bit3", 3)),
            NumberRegField(consts.HOST_RX_FLEXE_LOF_IMPL, self.getaddr(134), RegBitField("Bit2", 2)),
            NumberRegField(consts.HOST_RX_FLEXE_LOM_IMPL, self.getaddr(134), RegBitField("Bit1", 1)),
            NumberRegField(consts.HOST_RX_FLEXE_LOPB_IMPL, self.getaddr(134), RegBitField("Bit0", 0)),
            NumberRegField(consts.HOST_TX_LOA_IMPL, self.getaddr(135), RegBitField("Bit2", 2)),
            NumberRegField(consts.HOST_TX_RF_IMPL, self.getaddr(135), RegBitField("Bit1", 1)),
            NumberRegField(consts.HOST_TX_LF_IMPL, self.getaddr(135), RegBitField("Bit0", 0)),
            NumberRegField(consts.HOST_RX_LOA_IMPL, self.getaddr(136), RegBitField("Bit2", 2)),
            NumberRegField(consts.HOST_RX_RF_IMPL, self.getaddr(136), RegBitField("Bit1", 1)),
            NumberRegField(consts.HOST_RX_LF_IMPL, self.getaddr(136), RegBitField("Bit0", 0)),
            NumberRegField(consts.RX_MSIM_IMPL, self.getaddr(137), RegBitField("Bit1", 1)),
            NumberRegField(consts.RX_CSTAT_CSF_IMPL, self.getaddr(137), RegBitField("Bit0", 0)),
            NumberRegField(consts.RX_PAYLOAD_TYPE_IMPL, self.getaddr(191), RegBitField("Bit0", 0)),
        ]
