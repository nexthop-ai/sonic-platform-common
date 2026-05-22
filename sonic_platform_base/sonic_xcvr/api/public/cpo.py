from sonic_platform_base.sonic_xcvr.api.public.cmis import CmisApi

class CpoApi(CmisApi):
    """
    An XcvrApi implementation for hardware with co-packaged optics (CPO) comprising of 
    an optical engine and an external laser source. This API can delegate to one, or both,
    APIs.
    """

    def __init__(self, optical_engine_xcvr_api, external_laser_source_xcvr_api) -> None:
        # We use the optical engine API as our "default" choice for existing CmisApi methods.
        super().__init__(optical_engine_xcvr_api.xcvr_eeprom)
        self.optical_engine_xcvr_api = optical_engine_xcvr_api
        self.external_laser_source_xcvr_api = external_laser_source_xcvr_api

    # TODO: Implement CPO specific methods

