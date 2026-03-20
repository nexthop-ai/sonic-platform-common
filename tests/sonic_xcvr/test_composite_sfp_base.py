"""
Test CompositeSfpBase module
"""

import pytest
from unittest.mock import MagicMock
from sonic_platform_base.sonic_xcvr.composite_sfp_base import CompositeSfpBase
from sonic_platform_base.sfp_base import SfpBase
from sonic_platform_base.sonic_xcvr.api.xcvr_api import XcvrApi


class ConcreteCompositeSfp(CompositeSfpBase):
    """Concrete implementation for testing abstract methods"""
    
    def __init__(self):
        SfpBase.__init__(self)
        self._devices = []
    
    def get_internal_devices(self):
        return self._devices
    
    def get_number_of_internal_devices(self):
        return len(self._devices)
    
    def get_internal_device(self, name):
        return MagicMock(spec=SfpBase)
    
    def get_xcvr_api(self):
        return MagicMock(spec=XcvrApi)


class TestCompositeSfpBase:
    """
    Collection of CompositeSfpBase test methods
    """
    
    def test_read_eeprom_raises_not_implemented(self):
        """Test that read_eeprom raises NotImplementedError"""
        composite_sfp = ConcreteCompositeSfp()
        
        with pytest.raises(NotImplementedError) as exc_info:
            composite_sfp.read_eeprom(0, 10)
        
        assert "CompositeSfp does not support direct eeprom access" in str(exc_info.value)
    
    def test_write_eeprom_raises_not_implemented(self):
        """Test that write_eeprom raises NotImplementedError"""
        composite_sfp = ConcreteCompositeSfp()
        
        with pytest.raises(NotImplementedError) as exc_info:
            composite_sfp.write_eeprom(0, 10, b'\x00' * 10)
        
        assert "CompositeSfp does not support direct eeprom access" in str(exc_info.value)
