import abc
import typing
from sonic_platform_base.sfp_base import SfpBase
from sonic_platform_base.sonic_xcvr.api.xcvr_api import XcvrApi

class CompositeSfpBase(abc.ABC, SfpBase):
    """
    Interface for a class that composes multiple SfpBase derived objects
    to present a single logical transceiver.
    """

    @abc.abstractmethod
    def get_internal_devices(self) -> typing.List[SfpBase]:
        """
        Get a list of all internal Sfp objects that this composite class is
        responsible for.
        """
        ...
  
    @abc.abstractmethod
    def get_number_of_internal_devices(self) -> int:
        """
        Get the number of internal Sfp objects that this composite class is
        responsible for.
        """
        ...

    @abc.abstractmethod
    def get_internal_device(self, name: str) -> SfpBase:
        """
        Get a specific internal Sfp object that this composite class is
        responsible for.

        The indexing/naming scheme for the internal devices is left up to the
        implementing class.
        """
        ...

    @abc.abstractmethod
    def get_xcvr_api(self) -> XcvrApi:
        """
        Subclasses should implement this method so that a custom xcvr API can
        be exposed for this composite Sfp. This xcvr API will provide a single
        unified API for the underlying devices.
        """
        ...

    def refresh_xcvr_api(self):
        self._xcvr_api = self.get_xcvr_api()

    def read_eeprom(self, offset, num_bytes):
        """
        Composite SFPs do not support direct eeprom access, since they are logical
        entities composed of multiple underlying devices. Instead, users should
        fetch internal devices directly via the get_internal_devices() or
        get_internal_device() methods and read eeprom from those devices as needed.
        """
        raise NotImplementedError("CompositeSfp does not support direct eeprom access.")

    def write_eeprom(self, offset, num_bytes, write_buffer):
        """
        Composite SFPs do not support direct eeprom access, since they are logical
        entities composed of multiple underlying devices. Instead, users should
        fetch internal devices directly via the get_internal_devices() or
        get_internal_device() methods and write eeprom from those devices as needed.
        """
        raise NotImplementedError("CompositeSfp does not support direct eeprom access.")
