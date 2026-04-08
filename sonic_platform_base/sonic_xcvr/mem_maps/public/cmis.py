"""
    cmis.py

    Implementation of XcvrMemMap for CMIS Rev 5.0
"""

from ..xcvr_mem_map import XcvrMemMap
from ...fields.xcvr_field import (
    RegGroupField,
)
from ...fields import consts
from ...fields.consts import *
from ...fields.public.cmis import CableLenField
from .cmis_pages.base import CMIS_NUM_BANKED_PAGES, get_field_from_pages

# Import page classes
from .cmis_pages import (
    CmisAdministrativeLowerPage,
    CmisAdministrativeUpperPage,
    CmisAdvertisingPage,
    CmisThresholdsPage,
    CmisLaneDatapathConfigPage,
    CmisLaneDatapathStatusPage,
    CmisTunableLaserCtrlStatusPage,
    CmisModulePerfDiagCtrlPage,
    CmisVdmAdvertisingCtrlPage,
    CmisCdbMessagePage,
)

class CmisFlatMemMap(XcvrMemMap):
    """
    Memory map for CMIS flat memory (Lower page and Upper page 0h ONLY)
    Now uses page-based architecture with CmisPage00Lower and CmisPage00Upper
    """
    def __init__(self, codes):
        super(CmisFlatMemMap, self).__init__(codes)

        # Create page instances
        self.administrative_lower_page = CmisAdministrativeLowerPage(codes)
        self.administrative_upper_page = CmisAdministrativeUpperPage(codes)

        # Build RegGroupFields from page instances
        self.MGMT_CHARACTERISTICS = RegGroupField(consts.MGMT_CHAR_FIELD,
            *get_field_from_pages(consts.MGMT_CHAR_FIELD, self.administrative_lower_page)
        )

        # ADMIN_INFO combines fields from both lower and upper pages
        # Also includes APPLS_ADVT_FIELD as a nested RegGroupField for backwards compatibility
        admin_info_fields = []
        admin_info_fields.extend(get_field_from_pages(consts.ADMIN_INFO_FIELD, self.administrative_lower_page, self.administrative_upper_page))

        # Add APPLS_ADVT_FIELD as a nested RegGroupField
        appls_advt_fields = get_field_from_pages(consts.APPLS_ADVT_FIELD, self.administrative_lower_page)
        if appls_advt_fields:
            admin_info_fields.append(RegGroupField(consts.APPLS_ADVT_FIELD, *appls_advt_fields))

        self.ADMIN_INFO = RegGroupField(consts.ADMIN_INFO_FIELD, *admin_info_fields)

        self.PAGE0_MODULE_LEVEL_MONITORS = RegGroupField(consts.MODULE_MONITORS_PAGE0_FIELD,
            *get_field_from_pages(consts.MODULE_MONITORS_PAGE0_FIELD, self.administrative_lower_page)
        )

        self.TRANS_MODULE_STATUS = RegGroupField(consts.TRANS_MODULE_STATUS_FIELD,
            *get_field_from_pages(consts.TRANS_MODULE_STATUS_FIELD, self.administrative_lower_page)
        )

        self.TRANS_CONFIG = RegGroupField(consts.TRANS_CONFIG_FIELD,
            *get_field_from_pages(consts.TRANS_CONFIG_FIELD, self.administrative_lower_page)
        )

        self.EXTENDED_MODULE_INFO = RegGroupField(consts.EXTENDED_MODULE_INFO_FIELD,
            *get_field_from_pages(consts.EXTENDED_MODULE_INFO_FIELD, self.administrative_lower_page)
        )

    @property
    def bank(self):
        """Returns the bank number (read-only)."""
        return self._bank

    def getaddr(self, page, offset, page_size=128):
        """
        Calculate linear offset for CMIS memory map using instance's bank.

        For bank 0: linear_offset = page * 128 + byte_offset
        For bank > 0 (pages 10h-FFh only):
            linear_offset = (bank * CMIS_NUM_BANKED_PAGES + page) * 128 + byte_offset

        Note: Pages 00h-0Fh are never banked, even for bank > 0.
        """
        if page == 0 and offset < 128:
            # Lower memory - not affected by banking
            return offset

        if self.bank == 0:
            # Bank 0: standard linear offset
            return page * page_size + offset
        else:
            # Banks 1+: only pages 10h-FFh (0x10+) are banked
            # Pages < 0x10 are never banked, even for bank > 0
            if page < 0x10:
                # Non-banked pages (00h-0Fh): same as bank 0
                return page * page_size + offset
            else:
                # Banked pages (10h-FFh): offset by bank * CMIS_NUM_BANKED_PAGES pages
                return ((self.bank * CMIS_NUM_BANKED_PAGES) + page) * page_size + offset

class CmisMemMap(CmisFlatMemMap):
    def __init__(self, codes):
        super(CmisMemMap, self).__init__(codes)

        # Initialize page instances
        self.advertising_page = CmisAdvertisingPage(codes, bank=bank)  # 0x01
        self.thresholds_page = CmisThresholdsPage(codes, bank=bank)  # 0x02
        self.datapath_control_page = CmisLaneDatapathConfigPage(codes, bank=bank)  # 0x10
        self.datapath_status_page = CmisLaneDatapathStatusPage(codes, bank=bank)  # 0x11
        self.tunable_module_monitors_page = CmisTunableLaserCtrlStatusPage(codes, bank=bank)  # 0x12
        self.loopback_page = CmisModulePerfDiagCtrlPage(codes, bank=bank)  # 0x13
        self.performance_monitoring_page = CmisVdmAdvertisingCtrlPage(codes, bank=bank)  # 0x2F
        self.cdb_message_page = CmisCdbMessagePage(codes, bank=bank)  # 0x9F

        # This memmap should contain ONLY upper page >= 01h fields
        self.ADVERTISING = RegGroupField(consts.ADVERTISING_FIELD,
            *get_field_from_pages(consts.ADVERTISING_FIELD, self.advertising_page, self.datapath_status_page)
        )

        self.MODULE_LEVEL_MONITORS = RegGroupField(consts.MODULE_MONITORS_FIELD,
            *get_field_from_pages(consts.MODULE_MONITORS_FIELD, self.tunable_module_monitors_page, self.advertising_page)
        )

        self.MODULE_CHAR_ADVT = RegGroupField(consts.MODULE_CHAR_ADVT_FIELD,
            *get_field_from_pages(consts.MODULE_CHAR_ADVT_FIELD, self.advertising_page)
        )

        self.THRESHOLDS = RegGroupField(consts.THRESHOLDS_FIELD,
            *get_field_from_pages(consts.THRESHOLDS_FIELD, self.thresholds_page)
        )

        self.LANE_DATAPATH_CTRL = RegGroupField(consts.LANE_DATAPATH_CTRL_FIELD,
            *get_field_from_pages(consts.LANE_DATAPATH_CTRL_FIELD, self.datapath_control_page)
        )

        self.TX_POWER_ALARM_FLAGS = RegGroupField(consts.TX_POWER_ALARM_FLAGS_FIELD,
            *get_field_from_pages(consts.TX_POWER_ALARM_FLAGS_FIELD, self.datapath_status_page)
        )

        self.TX_BIAS_ALARM_FLAGS = RegGroupField(consts.TX_BIAS_ALARM_FLAGS_FIELD,
            *get_field_from_pages(consts.TX_BIAS_ALARM_FLAGS_FIELD, self.datapath_status_page)
        )

        self.RX_POWER_ALARM_FLAGS = RegGroupField(consts.RX_POWER_ALARM_FLAGS_FIELD,
            *get_field_from_pages(consts.RX_POWER_ALARM_FLAGS_FIELD, self.datapath_status_page)
        )

        self.LANE_DATAPATH_STATUS = RegGroupField(consts.LANE_DATAPATH_STATUS_FIELD,
            *get_field_from_pages(consts.LANE_DATAPATH_STATUS_FIELD, self.datapath_status_page, self.tunable_module_monitors_page)
        )

        self.TRANS_LOOPBACK = RegGroupField(consts.TRANS_LOOPBACK_FIELD,
            *get_field_from_pages(consts.TRANS_LOOPBACK_FIELD, self.loopback_page)
        )

        self.TRANS_PM = RegGroupField(consts.TRANS_PM_FIELD,
            *get_field_from_pages(consts.TRANS_PM_FIELD, self.performance_monitoring_page)
        )

        self.TRANS_CDB = RegGroupField(consts.TRANS_CDB_FIELD,
            *get_field_from_pages(consts.TRANS_CDB_FIELD, self.advertising_page, self.cdb_message_page)
        )

        self.STAGED_CTRL0 = RegGroupField("%s_%d" % (consts.STAGED_CTRL_FIELD, 0),
            *get_field_from_pages("%s_%d" % (consts.STAGED_CTRL_FIELD, 0), self.datapath_control_page)
        )

        self.SIGNAL_INTEGRITY_CTRL_ADVT = RegGroupField(consts.SIGNAL_INTEGRITY_CTRL_ADVT_FIELD,
            *get_field_from_pages(consts.SIGNAL_INTEGRITY_CTRL_ADVT_FIELD, self.advertising_page)
        )

        self.STAGED_CTRL0_TX_RX_CTRL = RegGroupField(consts.STAGED_CTRL0_TX_RX_CTRL_FIELD,
            *get_field_from_pages(consts.STAGED_CTRL0_TX_RX_CTRL_FIELD, self.datapath_control_page)
        )
        # TODO: add remaining fields

    def getaddr(self, page, offset, page_size=128):
        return page * page_size + offset
