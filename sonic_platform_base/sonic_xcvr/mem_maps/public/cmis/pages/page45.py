"""
    page45.py

    C-CMIS Page 45h - Host Lane Provisioning Advertisement.
"""

from .page import CmisPage
from .....fields.xcvr_field import NumberRegField, RegBitField
from .....fields import consts


class CCmisHostLaneProvisioningAdvertisementPage(CmisPage):
    """C-CMIS Page 45h: advertises which host-lane provisioning parameters are implemented."""

    def __init__(self, codes, bank=0, page=0x45):
        super().__init__(codes, page=page, bank=bank)

        self.fields[consts.HOST_LANE_PROVISIONING_ADVERTISEMENT] = [
            NumberRegField(consts.TX_FED_CONS_ACT_ENABLE_IMPL, self.getaddr(128), RegBitField("Bit5", 5)),
            NumberRegField(consts.RX_FED_CONS_ACT_ENABLE_IMPL, self.getaddr(128), RegBitField("Bit4", 4)),
            NumberRegField(consts.RX_LF_INSERTION_ON_CSF_ENABLE_IMPL, self.getaddr(128), RegBitField("Bit3", 3)),
            NumberRegField(consts.TX_LF_INSERTION_ON_LD_ENABLE_IMPL, self.getaddr(128), RegBitField("Bit2", 2)),
            NumberRegField(consts.FED_MON_ENABLE_IMPL, self.getaddr(128), RegBitField("Bit1", 1)),
            NumberRegField(consts.FDD_MON_ENABLE_IMPL, self.getaddr(128), RegBitField("Bit0", 0)),
            NumberRegField(consts.TX_CSTAT_LCK_INSERTION_IMPL, self.getaddr(129), RegBitField("Bit6", 6)),
            NumberRegField(consts.RX_RPLC_SIG_INSERTION_IMPL, self.getaddr(129), RegBitField("Bit5", 5)),
            NumberRegField(consts.TX_RPLC_SIG_INSERTION_IMPL, self.getaddr(129), RegBitField("Bit4", 4)),
            NumberRegField(consts.TX_CONS_ACT_HOLD_OFF_TMR_IMPL, self.getaddr(129), RegBitField("Bit3", 3)),
            NumberRegField(consts.RX_CONS_ACT_HOLD_OFF_TMR_IMPL, self.getaddr(129), RegBitField("Bit2", 2)),
            NumberRegField(consts.RX_CONS_ACT_IMPL, self.getaddr(129), RegBitField("Bit1", 1)),
            NumberRegField(consts.TX_CONS_ACT_IMPL, self.getaddr(129), RegBitField("Bit0", 0)),
        ]
