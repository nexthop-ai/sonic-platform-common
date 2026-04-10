import typing
from sonic_platform_base.sonic_xcvr.composite_sfp_base import CompositeSfpBase
from sonic_platform_base.sonic_xcvr.api.public.cpo import CpoApi
from sonic_platform_base.sfp_base import SfpBase

class CpoSfpBase(CompositeSfpBase, SfpBase):
    def __init__(self, oe: SfpBase, els: SfpBase) -> None:
        SfpBase.__init__(self)
        self._oe = oe
        self._els = els

    def get_internal_devices(self) -> typing.List[SfpBase]:
        return [self._oe, self._els]

    def get_number_of_internal_devices(self) -> int:
        return 2

    def get_internal_device(self, name: str) -> SfpBase:
        """
        The name parameter is used to determine which
        internal SFP device to return. It can be "OE"
        to fetch the optical engine or "ELS" to fetch
        the external laser source.
        """
        if name == "OE":
            return self._oe
        elif name == "ELS":
            return self._els
        raise ValueError(f"No SFP found for {name}")

    def get_xcvr_api(self):
        return CpoApi(
            optical_engine_xcvr_api=self._oe.get_xcvr_api(),
            external_laser_source_xcvr_api=self._els.get_xcvr_api()
        )

    # TODO: Implement CPO-specific methods here.

