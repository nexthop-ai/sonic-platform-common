from sonic_platform_base.sonic_xcvr.api.public.cmis import CmisApi
from sonic_platform_base.sonic_xcvr.api.public.elsfp import ElsfpApi

class CpoApi(CmisApi):
    """
    An XcvrApi implementation for hardware with co-packaged optics (CPO) comprising of 
    an optical engine and an external laser source.

    CPO hardware can have two modes:
        - separate mode: the optical engine and external laser source are both exposed to software
        independently. Software needs to manage them as separate entities.
        - joint mode: an internal hardware component (typically called an MCU) handles all I2C
        traffic, routing it to the appropriate underlying device (optical engine or laser) on
        behalf of the client.
    
    This class can be used for both modes.
        - for separate mode, pass in
            - a optical engine xcvr API populated with an optical engine
            memory map and eeprom read/write functions that access the optical engine sysfs path.
            - an external laser source xcvr API populated with an ELSFP memory map
            and eeprom read/write functions that access the elsfp sysfs path.
        - for joint mode, pass in
            - a optical engine xcvr API populated with an optical engine
            memory map and eeprom read/write functions that access the optical engine sysfs path.
            - an external laser source xcvr API populated with an ELSFP-aware optical engine
            memory map and eeprom read/write functions that access the optical engine sysfs path.
    """
    def __init__(self, optical_engine_xcvr_api, external_laser_source_xcvr_api) -> None:
        # We use the optical engine API as our "default" choice for existing CmisApi methods.
        super().__init__(optical_engine_xcvr_api.xcvr_eeprom)
        self.optical_engine_xcvr_api = optical_engine_xcvr_api
        self.external_laser_source_xcvr_api = external_laser_source_xcvr_api

    # TODO: Implement CPO specific methods

