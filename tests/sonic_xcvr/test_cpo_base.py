"""
Test CpoSfpBase module
"""

import pytest
from unittest.mock import MagicMock
from sonic_platform_base.sonic_xcvr.composite_sfp_base import CompositeSfpBase
from sonic_platform_base.sonic_xcvr.cpo_base import CpoSfpBase
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
        
        cpo_sfp = CpoSfpBase(oe=oe_sfp, els=els_sfp)
        
        assert cpo_sfp._oe is oe_sfp
        assert cpo_sfp._els is els_sfp
    
    def test_get_internal_devices(self):
        """Test get_internal_devices returns both OE and ELS devices"""
        oe_sfp = MagicMock(spec=SfpBase)
        els_sfp = MagicMock(spec=SfpBase)
        
        cpo_sfp = CpoSfpBase(oe=oe_sfp, els=els_sfp)
        devices = cpo_sfp.get_internal_devices()
        
        assert len(devices) == 2
        assert oe_sfp in devices
        assert els_sfp in devices
        assert devices[0] is oe_sfp
        assert devices[1] is els_sfp
    
    def test_get_number_of_internal_devices(self):
        """Test get_number_of_internal_devices returns 2"""
        oe_sfp = MagicMock(spec=SfpBase)
        els_sfp = MagicMock(spec=SfpBase)
        
        cpo_sfp = CpoSfpBase(oe=oe_sfp, els=els_sfp)
        
        assert cpo_sfp.get_number_of_internal_devices() == 2
    
    def test_get_internal_device_valid_names(self):
        """Test get_internal_device with valid OE and ELS names"""
        oe_sfp = MagicMock(spec=SfpBase)
        els_sfp = MagicMock(spec=SfpBase)
        
        cpo_sfp = CpoSfpBase(oe=oe_sfp, els=els_sfp)
        oe_device = cpo_sfp.get_internal_device("OE")
        els_device = cpo_sfp.get_internal_device("ELS")
        
        assert oe_device is oe_sfp
        assert els_device is els_sfp
    
    def test_get_internal_device_invalid_names(self):
        """Test get_internal_device raises ValueError for invalid names"""
        oe_sfp = MagicMock(spec=SfpBase)
        els_sfp = MagicMock(spec=SfpBase)
        
        cpo_sfp = CpoSfpBase(oe=oe_sfp, els=els_sfp)
        
        with pytest.raises(ValueError) as exc_info:
            cpo_sfp.get_internal_device("INVALID_DEVICE_NAME")
        
        assert f"No SFP found for INVALID_DEVICE_NAME" in str(exc_info.value)
