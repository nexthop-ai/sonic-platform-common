"""
    base.py

    Abstract class for CMIS pages
"""

from typing import Dict
from ...xcvr_mem_map import XcvrMemMap
from ....fields.xcvr_field import RegField
from .cmis_page_consts import CMIS_NUM_BANKED_PAGES

def get_field_from_pages(field_name, *pages):
        fields = []
        for page in pages:
            if hasattr(page, 'fields') and field_name in page.fields:
                fields.extend(page.fields[field_name])
        return fields

class CmisPage(XcvrMemMap):
    fields: Dict[str, list[RegField]]  # This is a Dictionary of list of fields

    def __init__(self, codes, page, bank):
        super(CmisPage, self).__init__(codes)
        self._page = page
        self._bank = bank
        self.fields = {}

    @property
    def page(self):
        """Returns the page number (read-only)."""
        return self._page

    @property
    def bank(self):
        """Returns the bank number (read-only)."""
        return self._bank

    def getaddr(self, offset, page_size=128):
        """
        Calculate linear offset for optoe driver using instance's bank.

        For bank 0: linear_offset = page * 128 + byte_offset
        For bank > 0 (pages 10h-FFh only):
            linear_offset = (bank * CMIS_NUM_BANKED_PAGES + page) * 128 + byte_offset

        Note: Pages 00h-0Fh are never banked, even for bank > 0.
        """
        if self._page == 0 and offset < 128:
            # Lower memory - not affected by banking
            return offset

        if self._bank == 0:
            # Bank 0: standard linear offset
            return self._page * page_size + offset
        else:
            # Banks 1+: only pages 10h-FFh (0x10+) are banked
            # Pages < 0x10 are never banked, even for bank > 0
            if self._page < 0x10:
                # Non-banked pages (00h-0Fh): same as bank 0
                return self._page * page_size + offset
            else:
                # Banked pages (10h-FFh): offset by bank * CMIS_NUM_BANKED_PAGES pages
                return ((self._bank * CMIS_NUM_BANKED_PAGES) + self._page) * page_size + offset

    def get_field_values(self, field: str):
        return self.fields[field]
