from sonic_platform_base.sonic_xcvr.optoe_eeprom_access import OptoeEepromAccessMixin
from sonic_platform_base.sonic_xcvr.cpo_base import OeBase, ElsfpBase

class OptoeOeBase(OeBase, OptoeEepromAccessMixin):
    pass

class OptoeElsfpBase(ElsfpBase, OptoeEepromAccessMixin):
    pass
