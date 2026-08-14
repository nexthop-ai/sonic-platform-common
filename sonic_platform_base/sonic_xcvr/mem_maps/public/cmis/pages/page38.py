"""
    page38.py

    C-CMIS Page 38h - Data Path Host Interface Configuration.
"""

from .page import CmisPage
from .....fields.xcvr_field import NumberRegField, RegBitField, RegBitsField
from .....fields import consts


class CCmisDataPathHostIfConfigPage(CmisPage):
    """C-CMIS Page 38h: host data-path degrade thresholds and consequent-action config."""

    def __init__(self, codes, bank=0, page=0x38):
        super().__init__(codes, page=page, bank=bank)

        # BER thresholds are F16; no F16 decoder exists, so exposed as raw U16.
        self.fields[consts.DATA_PATH_HOST_IF_CONFIG] = [
            NumberRegField(consts.FDD_ACT_BER_THRESH, self.getaddr(128), format=">H", size=2, ro=False),
            NumberRegField(consts.FDD_CLR_BER_THRESH, self.getaddr(130), format=">H", size=2, ro=False),
            NumberRegField(consts.FED_ACT_BER_THRESH, self.getaddr(132), format=">H", size=2, ro=False),
            NumberRegField(consts.FED_CLR_BER_THRESH, self.getaddr(134), format=">H", size=2, ro=False),
            NumberRegField(consts.HOST_FDD_FED_CONS_ACT_ENABLE, self.getaddr(136),
                RegBitField(consts.TX_FED_CONS_ACT_ENABLE, 5),
                RegBitField(consts.RX_FED_CONS_ACT_ENABLE, 4),
                RegBitField(consts.RX_LF_INSERTION_ON_CSF_ENABLE, 3),
                RegBitField(consts.TX_LF_INSERTION_ON_LD_ENABLE, 2),
                RegBitField(consts.FED_MON_ENABLE, 1, ro=False),
                RegBitField(consts.FDD_MON_ENABLE, 0, ro=False),
                ro=False),
            NumberRegField(consts.RX_CONS_ACT, self.getaddr(137), RegBitsField("Bits7-4", 4, size=4)),
            NumberRegField(consts.TX_CONS_ACT, self.getaddr(137), RegBitsField("Bits3-0", 0, size=4)),
            NumberRegField(consts.RX_CONS_ACT_HOLD_OFF_TMR, self.getaddr(141), format=">H", size=2),
            NumberRegField(consts.TX_CONS_ACT_HOLD_OFF_TMR, self.getaddr(143), format=">H", size=2),
            NumberRegField(consts.RX_RPLC_SIG_INSERTION, self.getaddr(145), RegBitsField("Bits7-4", 4, size=4)),
            NumberRegField(consts.TX_RPLC_SIG_INSERTION, self.getaddr(145), RegBitsField("Bits3-0", 0, size=4)),
            NumberRegField(consts.TX_CSTAT_LCK_INSERTION, self.getaddr(146), RegBitsField("Bits3-0", 0, size=4)),
        ]
