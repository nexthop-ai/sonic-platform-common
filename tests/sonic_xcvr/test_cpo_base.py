"""
Test CpoSfpBase module
"""

import pytest
from unittest.mock import MagicMock
from sonic_platform_base.sonic_xcvr.cpo_base import CpoSfpBase
from sonic_platform_base.sonic_xcvr.cpo_xcvr_api_factory import CpoHardwareId
from sonic_platform_base.sfp_base import SfpBase
from sonic_platform_base.sonic_xcvr.api.xcvr_api import XcvrApi


class TestCpoSfpBase:
    """
    Collection of CpoSfpBase test methods
    """
    
    def test_cpo_sfp_initialization(self):
        """Test CpoSfpBase initialization with optical engine and external laser source"""
        oe_sfp = MagicMock(spec=SfpBase)
        els_sfp = MagicMock(spec=SfpBase)
        hardware_id = MagicMock(spec=CpoHardwareId)

        cpo_sfp = CpoSfpBase(oe=oe_sfp, elsfp=els_sfp, hardware_id=hardware_id)

        assert cpo_sfp.oe is oe_sfp
        assert cpo_sfp.elsfp is els_sfp
        assert cpo_sfp.hardware_id is hardware_id
