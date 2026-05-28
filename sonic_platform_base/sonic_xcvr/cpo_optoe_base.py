from sonic_platform_base.sonic_xcvr.optoe_eeprom_rw import OptoeEepromReadWriteMixin
from sonic_platform_base.sonic_xcvr.cpo_base import OeBase, ElsfpBase, JointModeElsfpBase

class OptoeOeBase(OeBase, OptoeEepromReadWriteMixin):
    pass

class OptoeElsfpBase(ElsfpBase, OptoeEepromReadWriteMixin):
    pass

class OptoeJointModeElsfpBase(JointModeElsfpBase, OptoeEepromReadWriteMixin):
    pass
