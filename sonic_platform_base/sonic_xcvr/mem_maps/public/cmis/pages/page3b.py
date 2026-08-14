"""
    page3b.py

    C-CMIS Page 3Bh - Data Path Host Interface Flags, Masks and Status.
"""

from .page import CmisPage
from .....fields.xcvr_field import NumberRegField, RegBitField
from .....fields import consts


class CCmisDataPathHostIfFlagsPage(CmisPage):
    """C-CMIS Page 3Bh: host data-path alarm masks and latches."""

    def __init__(self, codes, bank=0, page=0x3B):
        super().__init__(codes, page=page, bank=bank)

        self.fields[consts.DATA_PATH_HOST_IF_FLAGS] = [
            # Byte 128: FEC degrade masks
            NumberRegField(consts.M_TX_FED_PM, self.getaddr(128), RegBitField("Bit1", 1)),
            NumberRegField(consts.M_TX_FDD_PM, self.getaddr(128), RegBitField("Bit0", 0)),
            # Byte 129: degrade / client masks
            NumberRegField(consts.M_RX_RD, self.getaddr(129), RegBitField("Bit6", 6)),
            NumberRegField(consts.M_TR_LD, self.getaddr(129), RegBitField("Bit5", 5)),
            NumberRegField(consts.M_RX_CSTAT_MNT_LCK, self.getaddr(129), RegBitField("Bit4", 4)),
            NumberRegField(consts.M_RX_MSIM, self.getaddr(129), RegBitField("Bit3", 3)),
            NumberRegField(consts.M_RX_CSTAT_CSF, self.getaddr(129), RegBitField("Bit2", 2)),
            NumberRegField(consts.M_TX_RD, self.getaddr(129), RegBitField("Bit1", 1)),
            NumberRegField(consts.M_TX_LD, self.getaddr(129), RegBitField("Bit0", 0)),
            # Byte 130: FlexE masks
            NumberRegField(consts.M_RX_FLEXE_RPF, self.getaddr(130), RegBitField("Bit7", 7)),
            NumberRegField(consts.M_RX_FLEXE_GID_MM, self.getaddr(130), RegBitField("Bit6", 6)),
            NumberRegField(consts.M_RX_FLEXE_INSTANCE_MAP_MM, self.getaddr(130), RegBitField("Bit5", 5)),
            NumberRegField(consts.M_RX_FLEXE_CALENDAR_MM, self.getaddr(130), RegBitField("Bit4", 4)),
            NumberRegField(consts.M_RX_FLEXE_IID_MM, self.getaddr(130), RegBitField("Bit3", 3)),
            NumberRegField(consts.M_RX_FLEXE_LOF, self.getaddr(130), RegBitField("Bit2", 2)),
            NumberRegField(consts.M_RX_FLEXE_LOM, self.getaddr(130), RegBitField("Bit1", 1)),
            NumberRegField(consts.M_RX_FLEXE_LOPB, self.getaddr(130), RegBitField("Bit0", 0)),
            # Byte 131: transmit fault/alignment masks
            NumberRegField(consts.M_TX_LOA, self.getaddr(131), RegBitField("Bit2", 2)),
            NumberRegField(consts.M_TX_RF, self.getaddr(131), RegBitField("Bit1", 1)),
            NumberRegField(consts.M_TX_LF, self.getaddr(131), RegBitField("Bit0", 0)),
            # Byte 132: receive fault/alignment masks
            NumberRegField(consts.M_RX_LOA, self.getaddr(132), RegBitField("Bit2", 2)),
            NumberRegField(consts.M_RX_RF, self.getaddr(132), RegBitField("Bit1", 1)),
            NumberRegField(consts.M_RX_LF, self.getaddr(132), RegBitField("Bit0", 0)),
            # Byte 192: latched FEC degrade over PM interval
            NumberRegField(consts.HOST_FDD_FED_FLAGS, self.getaddr(192),
                RegBitField(consts.L_TX_FED_PM, 1),
                RegBitField(consts.L_TX_FDD_PM, 0),
                bitdecode=True),
            # Byte 193: latched degrade / client
            NumberRegField(consts.L_RX_RD, self.getaddr(193), RegBitField("Bit6", 6)),
            NumberRegField(consts.L_RX_LD, self.getaddr(193), RegBitField("Bit5", 5)),
            NumberRegField(consts.L_RX_CSTAT_MNT_LCK, self.getaddr(193), RegBitField("Bit4", 4)),
            NumberRegField(consts.L_RX_MSIM, self.getaddr(193), RegBitField("Bit3", 3)),
            NumberRegField(consts.L_RX_CSTAT_CSF, self.getaddr(193), RegBitField("Bit2", 2)),
            NumberRegField(consts.L_TX_RD, self.getaddr(193), RegBitField("Bit1", 1)),
            NumberRegField(consts.L_TX_LD, self.getaddr(193), RegBitField("Bit0", 0)),
            # Byte 194: latched FlexE
            NumberRegField(consts.L_RX_FLEXE_RPF, self.getaddr(194), RegBitField("Bit7", 7)),
            NumberRegField(consts.L_RX_FLEXE_GID_MM, self.getaddr(194), RegBitField("Bit6", 6)),
            NumberRegField(consts.L_RX_FLEXE_INSTANCE_MAP_MM, self.getaddr(194), RegBitField("Bit5", 5)),
            NumberRegField(consts.L_RX_FLEXE_CALENDAR_MM, self.getaddr(194), RegBitField("Bit4", 4)),
            NumberRegField(consts.L_RX_FLEXE_IID_MM, self.getaddr(194), RegBitField("Bit3", 3)),
            NumberRegField(consts.L_RX_FLEXE_LOF, self.getaddr(194), RegBitField("Bit2", 2)),
            NumberRegField(consts.L_RX_FLEXE_LOM, self.getaddr(194), RegBitField("Bit1", 1)),
            NumberRegField(consts.L_RX_FLEXE_LOPB, self.getaddr(194), RegBitField("Bit0", 0)),
            # Byte 195: latched transmit fault/alignment
            NumberRegField(consts.L_TX_LOA_HOST, self.getaddr(195), RegBitField("Bit2", 2)),
            NumberRegField(consts.L_TX_RF, self.getaddr(195), RegBitField("Bit1", 1)),
            NumberRegField(consts.L_TX_LF, self.getaddr(195), RegBitField("Bit0", 0)),
            # Byte 196: latched receive fault/alignment
            NumberRegField(consts.L_RX_LOA_HOST, self.getaddr(196), RegBitField("Bit2", 2)),
            NumberRegField(consts.L_RX_RF, self.getaddr(196), RegBitField("Bit1", 1)),
            NumberRegField(consts.L_RX_LF, self.getaddr(196), RegBitField("Bit0", 0)),
        ]
