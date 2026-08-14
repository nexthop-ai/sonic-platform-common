"""
    c-cmis.py

    Implementation of XcvrApi that corresponds to C-CMIS
"""
from ...fields import consts
from .cmis import CmisApi, CMIS_VDM_KEY_TO_DB_PREFIX_KEY_MAP, CMIS_XCVR_INFO_DEFAULT_DICT
import time
import copy
<<<<<<< HEAD
=======
from ...utils.cache import read_only_cached_api_return
from ...utils.common import get_F16, set_F16
>>>>>>> 9322fc3 (NOS-11650: Updated C-CMIS FDD/FED memory maps and constants (#149))

C_CMIS_DELTA_VDM_KEY_TO_DB_PREFIX_KEY_MAP = {
    'Modulator Bias X/I [%]' : 'biasxi',
    'Modulator Bias X/Q [%]' : 'biasxq',
    'Modulator Bias X_Phase [%]' : 'biasxp',
    'Modulator Bias Y/I [%]' : 'biasyi',
    'Modulator Bias Y/Q [%]' : 'biasyq',
    'Modulator Bias Y_Phase [%]' : 'biasyp',
    'CD high granularity, short link [ps/nm]' : 'cdshort',
    'CD low granularity, long link [ps/nm]' : 'cdlong',
    'DGD [ps]' : 'dgd',
    'SOPMD [ps^2]' : 'sopmd',
    'SOP ROC [krad/s]' : 'soproc',
    'PDL [dB]' : 'pdl',
    'OSNR [dB]' : 'osnr',
    'eSNR [dB]' : 'esnr',
    'CFO [MHz]' : 'cfo',
    'Tx Power [dBm]' : 'txcurrpower',
    'Rx Total Power [dBm]' : 'rxtotpower',
    'Rx Signal Power [dBm]' : 'rxsigpower'
}

VDM_SUBTYPE_IDX_MAP= {
    1: 'highalarm',
    2: 'lowalarm',
    3: 'highwarning',
    4: 'lowwarning',
    5: 'highalarm_flag',
    6: 'lowalarm_flag',
    7: 'highwarning_flag',
    8: 'lowwarning_flag'
}

C_CMIS_XCVR_INFO_DEFAULT_DICT = copy.deepcopy(CMIS_XCVR_INFO_DEFAULT_DICT)
C_CMIS_XCVR_INFO_DEFAULT_DICT.update({
    "supported_max_tx_power": "N/A",
    "supported_min_tx_power": "N/A",
    "supported_max_laser_freq": "N/A",
    "supported_min_laser_freq": "N/A"
})

class CCmisApi(CmisApi):
    def __init__(self, xcvr_eeprom, init_cdb_fw_handler=False):
        super(CCmisApi, self).__init__(xcvr_eeprom, init_cdb_fw_handler)

    def _get_vdm_key_to_db_prefix_map(self):
        combined_map = {**CMIS_VDM_KEY_TO_DB_PREFIX_KEY_MAP, **C_CMIS_DELTA_VDM_KEY_TO_DB_PREFIX_KEY_MAP}
        return combined_map

    def get_freq_grid(self):
        '''
        This function returns the configured frequency grid. Unit in GHz
        '''
        freq_grid = self.xcvr_eeprom.read(consts.GRID_SPACING)
        if freq_grid == 8:
            return 150
        elif freq_grid == 7:
            return 75
        elif freq_grid == 6:
            return 33
        elif freq_grid == 5:
            return 100
        elif freq_grid == 4:
            return 50
        elif freq_grid == 3:
            return 25
        elif freq_grid == 2:
            return 12.5
        elif freq_grid == 1:
            return 6.25
        elif freq_grid == 0:
            return 3.125
        else:
            return None

    def get_laser_config_freq(self):
        '''
        This function returns the configured laser frequency. Unit in GHz
        '''
        freq_grid = self.get_freq_grid()
        channel = self.xcvr_eeprom.read(consts.LASER_CONFIG_CHANNEL)
        # OIF-CMIS 5.3 Table 8-66: 75GHz is 193.1 + n x 0.025 THz, but 150GHz
        # is 193.1 + (n+3) x 0.025 THz - the two grids are not interchangeable.
        if freq_grid == 75:
            config_freq = 193100 + channel * 25
        elif freq_grid == 150:
            config_freq = 193100 + (channel + 3) * 25
        else:
            # All other grids (100/50/25/12.5/6.25/3.125GHz) use a plain
            # 193.1 + n x grid formula with no additive offset.
            config_freq = 193100 + channel * freq_grid
        return config_freq

    def get_current_laser_freq(self):
        '''
        This function returns the monitored laser frequency. Unit in GHz
        '''
        return self.xcvr_eeprom.read(consts.LASER_CURRENT_FREQ)

    def get_tuning_in_progress(self):
        '''
        This function returns tuning in progress status on media lane
        False means tuning not in progress
        True means tuning in progress
        '''
        return bool(self.xcvr_eeprom.read(consts.TUNING_IN_PROGRESS))

    def get_wavelength_unlocked(self):
        '''
        This function returns wavelength unlocked status on media lane
        False means wavelength locked
        True means wavelength unlocked
        '''
        return bool(self.xcvr_eeprom.read(consts.WAVELENGTH_UNLOCKED))

    def get_laser_tuning_summary(self):
        '''
        This function returns laser tuning status summary on media lane
        '''
        result = self.xcvr_eeprom.read(consts.LASER_TUNING_DETAIL)
        laser_tuning_summary = []
        if (result >> 5) & 0x1:
            laser_tuning_summary.append("TargetOutputPowerOOR")
        if (result >> 4) & 0x1:
            laser_tuning_summary.append("FineTuningOutOfRange")
        if (result >> 3) & 0x1:
            laser_tuning_summary.append("TuningNotAccepted")
        if (result >> 2) & 0x1:
            laser_tuning_summary.append("InvalidChannel")
        if (result >> 1) & 0x1:
            laser_tuning_summary.append("WavelengthUnlocked")
        if (result >> 0) & 0x1:
            laser_tuning_summary.append("TuningComplete")
        return laser_tuning_summary

    def get_supported_freq_config(self):
        '''
        This function returns the supported freq grid, low and high supported channel in 75/100GHz grid,
        and low and high frequency supported in GHz.
        allowed channel number bound in 75/100 GHz grid
        allowed frequency bound in 75/100 GHz grid
        '''
        grid_supported = self.xcvr_eeprom.read(consts.SUPPORT_GRID)
        low_ch_num = self.xcvr_eeprom.read(consts.LOW_CHANNEL)
        hi_ch_num = self.xcvr_eeprom.read(consts.HIGH_CHANNEL)
        low_freq_supported = 193100 + low_ch_num * 25
        high_freq_supported = 193100 + hi_ch_num * 25
        return grid_supported, low_ch_num, hi_ch_num, low_freq_supported, high_freq_supported

    def set_laser_freq(self, freq, grid):
        '''
        This function sets the laser frequency. Unit in GHz
        ZR application will not support fine tuning of the laser
        SONiC will support 75 GHz, 100GHz and 150GHz frequency grids
        Return True if the provision succeeds, False if it fails
        '''
        grid_supported, low_ch_num, hi_ch_num, _, _ = self.get_supported_freq_config()
        grid_supported_75GHz = (grid_supported >> 7) & 0x1
        grid_supported_100GHz = (grid_supported >> 5) & 0x1
        if grid == 75:
            assert grid_supported_75GHz
            freq_grid = 0x70
            channel_number = int(round((freq - 193100)/25))
            assert channel_number % 3 == 0
        elif grid == 100:
            assert grid_supported_100GHz
            freq_grid = 0x50
            channel_number = int(round((freq - 193100)/100))
        elif grid == 150:
            freq_grid = 0x80
            # OIF-CMIS 5.3 Table 8-66: Frequency (THz) = 193.1 + (n+3) x 0.025,
            # so n = (freq - 193100) / 25 - 3, and n (not n+3) must be a
            # multiple of 6.
            channel_number = int(round((freq - 193100)/25)) - 3
            assert channel_number % 6 == 0
        else:
            return False
        self.xcvr_eeprom.write(consts.GRID_SPACING, freq_grid)
        if channel_number > hi_ch_num or channel_number < low_ch_num:
            raise ValueError('Provisioned frequency out of range. Max Freq: 196100; Min Freq: 191300 GHz.')
        status = self.xcvr_eeprom.write(consts.LASER_CONFIG_CHANNEL, channel_number)
        return status

    def set_tx_power(self, tx_power):
        '''
        This function sets the TX output power. Unit in dBm
        Return True if the provision succeeds, False if it fails
        '''
        status = self.xcvr_eeprom.write(consts.TX_CONFIG_POWER, tx_power)
        time.sleep(1)
        return status

<<<<<<< HEAD
=======
    @read_only_cached_api_return
    def _is_rx_clockrec_pm_implemented(self):
        '''
        Returns True if the Page 42h clock recovery loop PM advertisement bit is
        set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.RX_CLOCK_REC_IMPL)))

    @read_only_cached_api_return
    def _is_rx_lg_sopmd_pm_implemented(self):
        '''
        Returns True if the Page 42h low-granularity SOPMD PM advertisement bit is
        set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.RX_LG_SOPMD_IMPL)))

    @read_only_cached_api_return
    def _is_rx_snr_margin_pm_implemented(self):
        '''
        Returns True if the Page 42h SNR margin PM advertisement bit is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.RX_SNR_MARGIN_IMPL)))

    @read_only_cached_api_return
    def _is_rx_qfactor_pm_implemented(self):
        '''
        Returns True if the Page 42h Q-factor PM advertisement bit is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.RX_QFACTOR_IMPL)))

    @read_only_cached_api_return
    def _is_rx_qmargin_pm_implemented(self):
        '''
        Returns True if the Page 42h Q-margin PM advertisement bit is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.RX_QMARGIN_IMPL)))

    # FDD/FED PM Advertisement (page 42h)

    @read_only_cached_api_return
    def _is_media_rx_fdd_pm_implemented(self):
        '''
        Returns True if the Page 42h media-lane FDD pm advertisement bit is
        set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.RX_MEDIA_FDD_PM_IMPL)))

    @read_only_cached_api_return
    def _is_media_rx_fed_pm_implemented(self):
        '''
        Returns True if the Page 42h media-lane FED pm advertisement bit is
        set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.RX_MEDIA_FED_PM_IMPL)))

    @read_only_cached_api_return
    def _is_host_tx_fdd_pm_implemented(self):
        '''
        Returns True if the Page 42h host data-path FDD pm advertisement bit
        is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.TX_HOST_FDD_PM_IMPL)))

    @read_only_cached_api_return
    def _is_host_tx_fed_pm_implemented(self):
        '''
        Returns True if the Page 42h host data-path FED pm advertisement bit
        is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.TX_HOST_FED_PM_IMPL)))

    # FDD/FED Alarm Advertisement (page 44h)

    @read_only_cached_api_return
    def _is_media_rx_fdd_alm_implemented(self):
        '''
        Returns True if the Page 44h media-lane FDD alarm advertisement bit is
        set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.MEDIA_RX_FDD_ALM_IMPL)))

    @read_only_cached_api_return
    def _is_media_rx_fed_alm_implemented(self):
        '''
        Returns True if the Page 44h media-lane FED alarm advertisement bit is
        set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.MEDIA_RX_FED_ALM_IMPL)))

    @read_only_cached_api_return
    def _is_host_tx_fdd_alm_implemented(self):
        '''
        Returns True if the Page 44h host data-path FDD alarm advertisement bit
        is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.HOST_TX_FDD_ALM_IMPL)))

    @read_only_cached_api_return
    def _is_host_tx_fed_alm_implemented(self):
        '''
        Returns True if the Page 44h host data-path FED alarm advertisement bit
        is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.HOST_TX_FED_ALM_IMPL)))

    # Host Lane Provisioning Advertisement (page 45h)

    @read_only_cached_api_return
    def _is_fed_mon_enable_implemented(self):
        '''
        Returns True if the Page 45h FED monitoring enable advertisement bit is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.HOST_FED_MON_EN_IMPL)))
    
    @read_only_cached_api_return
    def _is_fdd_mon_enable_implemented(self):
        '''
        Returns True if the Page 45h FDD monitoring enable advertisement bit is set.
        '''
        return (self.is_coherent_module() and not self.is_flat_memory()
                and bool(self.xcvr_eeprom.read(consts.HOST_FDD_MON_EN_IMPL)))

    def get_supported_fdd_fed_ber_config(self):
        '''
        Returns the (min, max) BER threshold that the FDD/FED raise/clear knobs
        accept.
        '''
        return 0.0, 1.0

    def get_transceiver_media_fdd_fed_config(self):
        '''
        Returns the media-lane FDD/FED BER threshold configuration (Page 30h)
        '''
        config = dict()
        if self._is_media_rx_fdd_pm_implemented():
            config['media_fdd_raise_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FDD_RAISE_THRESH))
            config['media_fdd_clear_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FDD_CLEAR_THRESH))
            config['media_fdd_enable'] = bool(self.xcvr_eeprom.read(consts.FDD_ENABLE))
        if self._is_media_rx_fed_pm_implemented():
            config['media_fed_raise_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FED_RAISE_THRESH))
            config['media_fed_clear_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FED_CLEAR_THRESH))
            config['media_fed_enable'] = bool(self.xcvr_eeprom.read(consts.FED_ENABLE))
        return config

    def get_transceiver_media_fdd_fed_flags(self):
        '''
        Returns the latched media-lane FDD/FED PM flags (Page 33h)
        '''
        fdd_supported = self._is_media_rx_fdd_alm_implemented()
        fed_supported = self._is_media_rx_fed_alm_implemented()
        if not fdd_supported and not fed_supported:
            return {}
        values = self.xcvr_eeprom.read(consts.MEDIA_FDD_FED_FLAGS)
        if values is None:
            return None
        flags = dict()
        if fdd_supported:
            flags['media_rx_fdd_asserted'] = bool(values[consts.L_RX_FDD_PM])
        if fed_supported:
            flags['media_rx_fed_asserted'] = bool(values[consts.L_RX_FED_PM])
        return flags

    def get_transceiver_host_fdd_fed_config(self):
        '''
        Returns the host data-path FDD/FED BER threshold configuration (Page 38h)
        '''
        config = dict()
        if self._is_host_tx_fdd_pm_implemented():
            config['host_fdd_act_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FDD_ACT_BER_THRESH))
            config['host_fdd_clear_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FDD_CLR_BER_THRESH))
            config['host_fdd_enable'] = bool(self.xcvr_eeprom.read(consts.FDD_MON_ENABLE))
        if self._is_host_tx_fed_pm_implemented():
            config['host_fed_act_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FED_ACT_BER_THRESH))
            config['host_fed_clear_thresh'] = get_F16(self.xcvr_eeprom.read(consts.FED_CLR_BER_THRESH))
            config['host_fed_enable'] = bool(self.xcvr_eeprom.read(consts.FED_MON_ENABLE))
        return config

    def get_transceiver_host_fdd_fed_flags(self):
        '''
        Returns the latched host data-path FDD/FED PM flags (Page 3Bh)
        '''
        values = self.xcvr_eeprom.read(consts.HOST_FDD_FED_FLAGS)
        if values is None:
            return {}
        flags = dict()
        if self._is_host_tx_fdd_alm_implemented():
            flags['host_tx_fdd_asserted'] = bool(values[consts.L_TX_FDD_PM])
        if self._is_host_tx_fed_alm_implemented():
            flags['host_tx_fed_asserted'] = bool(values[consts.L_TX_FED_PM])
        return flags

    def get_transceiver_fdd_fed_config(self):
        '''
        Returns the combined media-lane and host data-path FDD/FED BER threshold
        configuration. Only the sides the module advertises are present.
        '''
        config = dict()
        config.update(self.get_transceiver_media_fdd_fed_config())
        config.update(self.get_transceiver_host_fdd_fed_config())
        return config

    def get_transceiver_fdd_fed_flags(self):
        '''
        Returns the combined latched media-lane and host data-path FDD/FED PM
        flags. Only the sides the module advertises are present.
        '''
        flags = dict()
        flags.update(self.get_transceiver_media_fdd_fed_flags())
        flags.update(self.get_transceiver_host_fdd_fed_flags())
        return flags

    def _write_ber_threshold(self, field, value):
        '''
        Encodes value as F16 and writes it to field.
        Returns True on success, False if the value is out of range or the
        write fails.
        '''
        raw = set_F16(value)
        if raw is None:
            return False
        return self._write_and_verify(field, raw)

    def _write_and_verify(self, field, value):
        '''Write a configuration field and verify that the module accepted it.'''
        try:
            if not self.xcvr_eeprom.write(field, value):
                return False
            time.sleep(0.01)
            readback = self.xcvr_eeprom.read(field)
        except (AssertionError, KeyError, TypeError, ValueError):
            return False
        if readback is None:
            return False
        if isinstance(readback, bool):
            return readback == bool(value)
        return readback == value

    def set_transceiver_media_fdd_fed_config(self, config):
        '''
        Writes media-lane FDD/FED BER threshold configuration (Page 30h)
        '''
        if not isinstance(config, dict):
            return False
        status = True

        fdd_keys = ('media_fdd_raise_thresh', 'media_fdd_clear_thresh', 'media_fdd_enable')
        if any(k in config for k in fdd_keys):
            fdd_supported = self._is_media_rx_fdd_pm_implemented()
            if not fdd_supported:
                status = False
            raise_ber = config.get('media_fdd_raise_thresh')
            clear_ber = config.get('media_fdd_clear_thresh')
            if 'media_fdd_raise_thresh' in config and fdd_supported:
                status &= self._write_ber_threshold(consts.FDD_RAISE_THRESH, raise_ber)
            if 'media_fdd_clear_thresh' in config and fdd_supported:
                status &= self._write_ber_threshold(consts.FDD_CLEAR_THRESH, clear_ber)
            if 'media_fdd_enable' in config and fdd_supported:
                status &= self._write_and_verify(consts.FDD_ENABLE, int(bool(config['media_fdd_enable'])))

        fed_keys = ('media_fed_raise_thresh', 'media_fed_clear_thresh', 'media_fed_enable')
        if any(k in config for k in fed_keys):
            fed_supported = self._is_media_rx_fed_pm_implemented()
            if not fed_supported:
                status = False
            raise_ber = config.get('media_fed_raise_thresh')
            clear_ber = config.get('media_fed_clear_thresh')
            if 'media_fed_raise_thresh' in config and fed_supported:
                status &= self._write_ber_threshold(consts.FED_RAISE_THRESH, raise_ber)
            if 'media_fed_clear_thresh' in config and fed_supported:
                status &= self._write_ber_threshold(consts.FED_CLEAR_THRESH, clear_ber)
            if 'media_fed_enable' in config and fed_supported:
                status &= self._write_and_verify(consts.FED_ENABLE, int(bool(config['media_fed_enable'])))

        return status

    def set_transceiver_host_fdd_fed_config(self, config):
        '''
        Writes host data-path FDD/FED BER threshold configuration (Page 38h)
        '''
        if not isinstance(config, dict):
            return False
        status = True

        fdd_threshold_keys = ('host_fdd_act_thresh', 'host_fdd_clear_thresh')
        if any(k in config for k in fdd_threshold_keys):
            fdd_supported = self._is_host_tx_fdd_pm_implemented()
            if not fdd_supported:
                status = False
            act_ber = config.get('host_fdd_act_thresh')
            clr_ber = config.get('host_fdd_clear_thresh')
            if 'host_fdd_act_thresh' in config and fdd_supported:
                status &= self._write_ber_threshold(consts.FDD_ACT_BER_THRESH, act_ber)
            if 'host_fdd_clear_thresh' in config and fdd_supported:
                status &= self._write_ber_threshold(consts.FDD_CLR_BER_THRESH, clr_ber)
        if 'host_fdd_enable' in config:
            if not self._is_host_tx_fdd_pm_implemented():
                status = False
            else:
                status &= self._write_and_verify(consts.FDD_MON_ENABLE, int(bool(config['host_fdd_enable'])))

        fed_threshold_keys = ('host_fed_act_thresh', 'host_fed_clear_thresh')
        if any(k in config for k in fed_threshold_keys):
            fed_supported = self._is_host_tx_fed_pm_implemented()
            if not fed_supported:
                status = False
            act_ber = config.get('host_fed_act_thresh')
            clr_ber = config.get('host_fed_clear_thresh')
            if 'host_fed_act_thresh' in config and fed_supported:
                status &= self._write_ber_threshold(consts.FED_ACT_BER_THRESH, act_ber)
            if 'host_fed_clear_thresh' in config and fed_supported:
                status &= self._write_ber_threshold(consts.FED_CLR_BER_THRESH, clr_ber)
        if 'host_fed_enable' in config:
            if not self._is_host_tx_fed_pm_implemented():
                status = False
            else:
                status &= self._write_and_verify(consts.FED_MON_ENABLE, int(bool(config['host_fed_enable'])))

        return status

    def set_transceiver_fdd_fed_config(self, config):
        '''
        Convenience aggregator applying both media-lane and host data-path
        FDD/FED configuration present in config.

        Returns True if all requested writes succeed, False otherwise.
        '''
        if not isinstance(config, dict):
            return False
        status = True
        media_keys = ('media_fdd_raise_thresh', 'media_fdd_clear_thresh', 'media_fdd_enable',
                      'media_fed_raise_thresh', 'media_fed_clear_thresh', 'media_fed_enable')
        host_keys = ('host_fdd_act_thresh', 'host_fdd_clear_thresh', 'host_fdd_enable',
                     'host_fed_act_thresh', 'host_fed_clear_thresh', 'host_fed_enable')
        if any(k in config for k in media_keys):
            status &= self.set_transceiver_media_fdd_fed_config(config)
        if any(k in config for k in host_keys):
            status &= self.set_transceiver_host_fdd_fed_config(config)
        return status

>>>>>>> 9322fc3 (NOS-11650: Updated C-CMIS FDD/FED memory maps and constants (#149))
    def get_pm_all(self):
        '''
        This function returns the PMs reported in Page 34h and 35h in OIF C-CMIS document
        CD:     unit in ps/nm
        DGD:    unit in ps
        SOPMD:  unit in ps^2
        PDL:    unit in dB
        OSNR:   unit in dB
        ESNR:   unit in dB
        CFO:    unit in MHz
        TXpower:unit in dBm
        RXpower:unit in dBm
        RX sig power:   unit in dBm
        SOPROC: unit in krad/s
        MER:    unit in dB
        '''
        PM_dict = dict()

        rx_bits_pm = self.xcvr_eeprom.read(consts.RX_BITS_PM)
        rx_bits_subint_pm = self.xcvr_eeprom.read(consts.RX_BITS_SUB_INTERVAL_PM)
        rx_corr_bits_pm = self.xcvr_eeprom.read(consts.RX_CORR_BITS_PM)
        rx_min_corr_bits_subint_pm = self.xcvr_eeprom.read(consts.RX_MIN_CORR_BITS_SUB_INTERVAL_PM)
        rx_max_corr_bits_subint_pm = self.xcvr_eeprom.read(consts.RX_MAX_CORR_BITS_SUB_INTERVAL_PM)

        if (rx_bits_subint_pm != 0) and (rx_bits_pm != 0):
            PM_dict['preFEC_BER_avg'] = rx_corr_bits_pm*1.0/rx_bits_pm
            PM_dict['preFEC_BER_min'] = rx_min_corr_bits_subint_pm*1.0/rx_bits_subint_pm
            PM_dict['preFEC_BER_max'] = rx_max_corr_bits_subint_pm*1.0/rx_bits_subint_pm
        # when module is low power, still need these values to show 1.0
        else:
            PM_dict['preFEC_BER_avg'] = 1.0
            PM_dict['preFEC_BER_min'] = 1.0
            PM_dict['preFEC_BER_max'] = 1.0
        rx_frames_pm = self.xcvr_eeprom.read(consts.RX_FRAMES_PM)
        rx_frames_subint_pm = self.xcvr_eeprom.read(consts.RX_FRAMES_SUB_INTERVAL_PM)
        rx_frames_uncorr_err_pm = self.xcvr_eeprom.read(consts.RX_FRAMES_UNCORR_ERR_PM)
        rx_min_frames_uncorr_err_subint_pm = self.xcvr_eeprom.read(consts.RX_MIN_FRAMES_UNCORR_ERR_SUB_INTERVAL_PM)
        rx_max_frames_uncorr_err_subint_pm = self.xcvr_eeprom.read(consts.RX_MAX_FRAMES_UNCORR_ERR_SUB_INTERVAL_PM)

        if (rx_frames_subint_pm != 0) and (rx_frames_pm != 0):
            PM_dict['preFEC_uncorr_frame_ratio_avg'] = rx_frames_uncorr_err_pm*1.0/rx_frames_subint_pm
            PM_dict['preFEC_uncorr_frame_ratio_min'] = rx_min_frames_uncorr_err_subint_pm*1.0/rx_frames_subint_pm
            PM_dict['preFEC_uncorr_frame_ratio_max'] = rx_max_frames_uncorr_err_subint_pm*1.0/rx_frames_subint_pm
        # when module is low power, still need these values
        else:
            PM_dict['preFEC_uncorr_frame_ratio_avg'] = 0
            PM_dict['preFEC_uncorr_frame_ratio_min'] = 0
            PM_dict['preFEC_uncorr_frame_ratio_max'] = 0
        PM_dict['rx_cd_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_CD_PM)
        PM_dict['rx_cd_min'] = self.xcvr_eeprom.read(consts.RX_MIN_CD_PM)
        PM_dict['rx_cd_max'] = self.xcvr_eeprom.read(consts.RX_MAX_CD_PM)

        PM_dict['rx_dgd_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_DGD_PM)
        PM_dict['rx_dgd_min'] = self.xcvr_eeprom.read(consts.RX_MIN_DGD_PM)
        PM_dict['rx_dgd_max'] = self.xcvr_eeprom.read(consts.RX_MAX_DGD_PM)

        PM_dict['rx_sopmd_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_SOPMD_PM)
        PM_dict['rx_sopmd_min'] = self.xcvr_eeprom.read(consts.RX_MIN_SOPMD_PM)
        PM_dict['rx_sopmd_max'] = self.xcvr_eeprom.read(consts.RX_MAX_SOPMD_PM)

        PM_dict['rx_pdl_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_PDL_PM)
        PM_dict['rx_pdl_min'] = self.xcvr_eeprom.read(consts.RX_MIN_PDL_PM)
        PM_dict['rx_pdl_max'] = self.xcvr_eeprom.read(consts.RX_MAX_PDL_PM)

        PM_dict['rx_osnr_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_OSNR_PM)
        PM_dict['rx_osnr_min'] = self.xcvr_eeprom.read(consts.RX_MIN_OSNR_PM)
        PM_dict['rx_osnr_max'] = self.xcvr_eeprom.read(consts.RX_MAX_OSNR_PM)

        PM_dict['rx_esnr_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_ESNR_PM)
        PM_dict['rx_esnr_min'] = self.xcvr_eeprom.read(consts.RX_MIN_ESNR_PM)
        PM_dict['rx_esnr_max'] = self.xcvr_eeprom.read(consts.RX_MAX_ESNR_PM)

        PM_dict['rx_cfo_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_CFO_PM)
        PM_dict['rx_cfo_min'] = self.xcvr_eeprom.read(consts.RX_MIN_CFO_PM)
        PM_dict['rx_cfo_max'] = self.xcvr_eeprom.read(consts.RX_MAX_CFO_PM)

        PM_dict['rx_evm_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_EVM_PM)
        PM_dict['rx_evm_min'] = self.xcvr_eeprom.read(consts.RX_MIN_EVM_PM)
        PM_dict['rx_evm_max'] = self.xcvr_eeprom.read(consts.RX_MAX_EVM_PM)

        PM_dict['tx_power_avg'] = self.xcvr_eeprom.read(consts.TX_AVG_POWER_PM)
        PM_dict['tx_power_min'] = self.xcvr_eeprom.read(consts.TX_MIN_POWER_PM)
        PM_dict['tx_power_max'] = self.xcvr_eeprom.read(consts.TX_MAX_POWER_PM)

        PM_dict['rx_power_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_POWER_PM)
        PM_dict['rx_power_min'] = self.xcvr_eeprom.read(consts.RX_MIN_POWER_PM)
        PM_dict['rx_power_max'] = self.xcvr_eeprom.read(consts.RX_MAX_POWER_PM)

        PM_dict['rx_sigpwr_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_SIG_POWER_PM)
        PM_dict['rx_sigpwr_min'] = self.xcvr_eeprom.read(consts.RX_MIN_SIG_POWER_PM)
        PM_dict['rx_sigpwr_max'] = self.xcvr_eeprom.read(consts.RX_MAX_SIG_POWER_PM)

        PM_dict['rx_soproc_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_SOPROC_PM)
        PM_dict['rx_soproc_min'] = self.xcvr_eeprom.read(consts.RX_MIN_SOPROC_PM)
        PM_dict['rx_soproc_max'] = self.xcvr_eeprom.read(consts.RX_MAX_SOPROC_PM)

        PM_dict['rx_mer_avg'] = self.xcvr_eeprom.read(consts.RX_AVG_MER_PM)
        PM_dict['rx_mer_min'] = self.xcvr_eeprom.read(consts.RX_MIN_MER_PM)
        PM_dict['rx_mer_max'] = self.xcvr_eeprom.read(consts.RX_MAX_MER_PM)
        return PM_dict

    def _get_xcvr_info_default_dict(self):
        return C_CMIS_XCVR_INFO_DEFAULT_DICT

    def get_transceiver_info(self):
        """
        Retrieves transceiver info of this SFP

        Returns:
            A dict which contains following keys/values :
        ================================================================================
        key                          = TRANSCEIVER_INFO|ifname  ; information for module on port
        ; field                      = value
        module_media_type            = 1*255VCHAR               ; module media interface ID
        host_electrical_interface    = 1*255VCHAR               ; host electrical interface ID
        media_interface_code         = 1*255VCHAR               ; media interface code
        host_lane_count              = INTEGER                  ; host lane count
        media_lane_count             = INTEGER                  ; media lane count
        host_lane_assignment_option  = INTEGER                  ; permissible first host lane number for application
        media_lane_assignment_option = INTEGER                  ; permissible first media lane number for application
        active_apsel_hostlane1       = INTEGER                  ; active application selected code assigned to host lane 1
        active_apsel_hostlane2       = INTEGER                  ; active application selected code assigned to host lane 2
        active_apsel_hostlane3       = INTEGER                  ; active application selected code assigned to host lane 3
        active_apsel_hostlane4       = INTEGER                  ; active application selected code assigned to host lane 4
        active_apsel_hostlane5       = INTEGER                  ; active application selected code assigned to host lane 5
        active_apsel_hostlane6       = INTEGER                  ; active application selected code assigned to host lane 6
        active_apsel_hostlane7       = INTEGER                  ; active application selected code assigned to host lane 7
        active_apsel_hostlane8       = INTEGER                  ; active application selected code assigned to host lane 8
        media_interface_technology   = 1*255VCHAR               ; media interface technology
        hardwarerev                  = 1*255VCHAR               ; module hardware revision 
        serialnum                    = 1*255VCHAR               ; module serial number 
        manufacturename              = 1*255VCHAR               ; module venndor name
        modelname                    = 1*255VCHAR               ; module model name
        vendor_rev                   = 1*255VCHAR               ; module vendor revision
        vendor_oui                   = 1*255VCHAR               ; vendor organizationally unique identifier
        vendor_date                  = 1*255VCHAR               ; module manufacture date
        connector_type               = 1*255VCHAR               ; connector type
        specification_compliance     = 1*255VCHAR               ; electronic or optical interfaces that supported
        active_firmware              = 1*255VCHAR               ; active firmware
        inactive_firmware            = 1*255VCHAR               ; inactive firmware
        supported_max_tx_power       = FLOAT                    ; support maximum tx power
        supported_min_tx_power       = FLOAT                    ; support minimum tx power
        supported_max_laser_freq     = FLOAT                    ; support maximum laser frequency
        supported_min_laser_freq     = FLOAT                    ; support minimum laser frequency
        ================================================================================
        """
        xcvr_info = super(CCmisApi, self).get_transceiver_info()

        # Return None if CmisApi class returns None, this indicates to XCVRD that retry is
        # needed.
        if xcvr_info is None:
            return None

        min_power, max_power = self.get_supported_power_config() or (None, None)
        _, _, _, low_freq_supported, high_freq_supported = self.get_supported_freq_config()
        xcvr_info.update({
            'supported_max_tx_power': max_power,
            'supported_min_tx_power': min_power,
            'supported_max_laser_freq': high_freq_supported,
            'supported_min_laser_freq': low_freq_supported
        })
        return xcvr_info

    def get_transceiver_dom_real_value(self):
        """
        Retrieves DOM sensor values for this transceiver

        The returned dictionary contains floating-point values corresponding to various
        DOM sensor readings, as defined in the TRANSCEIVER_DOM_SENSOR table in STATE_DB.

        Returns:
            Dictionary
        """
        trans_dom = super(CCmisApi,self).get_transceiver_dom_real_value()

        trans_dom['laser_config_freq'] = self.get_laser_config_freq()
        trans_dom['laser_curr_freq'] = self.get_current_laser_freq()
        trans_dom['tx_config_power'] = self.get_tx_config_power()
        return trans_dom

    def get_transceiver_status(self):
        """
        Retrieves the current status of the transceiver module.

        Accesses non-latched registers to gather information about the module's state,
        fault causes, and datapath-level statuses, including TX and RX statuses.

        Returns:
            dict: A dictionary containing boolean values for various status fields, as defined in
                the TRANSCEIVER_STATUS table in STATE_DB.
        If there is an issue with reading the xcvr, None should be returned.
        """
        trans_status = super(CCmisApi,self).get_transceiver_status()
        trans_status['tuning_in_progress'] = self.get_tuning_in_progress()
        trans_status['wavelength_unlock_status'] = self.get_wavelength_unlocked()

        return trans_status

    def get_transceiver_status_flags(self):
        """
        Retrieves the current flag status of the transceiver module.

        Accesses latched registers to gather information about both
        module-level and datapath-level states (including TX/RX related flags).

        Returns:
            dict: A dictionary containing boolean values for various flags, as defined in
                the TRANSCEIVER_STATUS_FLAGS table in STATE_DB.
        """
        status_flags_dict = super().get_transceiver_status_flags()

        laser_tuning_summary = self.get_laser_tuning_summary()
        status_flags_dict.update({
            'target_output_power_oor': 'TargetOutputPowerOOR' in laser_tuning_summary,
            'fine_tuning_oor': 'FineTuningOutOfRange' in laser_tuning_summary,
            'tuning_not_accepted': 'TuningNotAccepted' in laser_tuning_summary,
            'invalid_channel_num': 'InvalidChannel' in laser_tuning_summary,
            'tuning_complete': 'TuningComplete' in laser_tuning_summary
        })

        return status_flags_dict

    def get_transceiver_pm(self):
        """
        Retrieves PM for this xcvr

        Returns:
            A dict containing the following keys/values :
        ========================================================================
        key                          = TRANSCEIVER_PM|ifname            ; information of PM on port
        ; field                      = value 
        prefec_ber_avg               = FLOAT                            ; prefec ber avg
        prefec_ber_min               = FLOAT                            ; prefec ber min
        prefec_ber_max               = FLOAT                            ; prefec ber max
        uncorr_frames_avg            = FLOAT                            ; uncorrected frames ratio avg
        uncorr_frames_min            = FLOAT                            ; uncorrected frames ratio min
        uncorr_frames_max            = FLOAT                            ; uncorrected frames ratio max
        cd_avg                       = FLOAT                            ; chromatic dispersion avg
        cd_min                       = FLOAT                            ; chromatic dispersion min
        cd_max                       = FLOAT                            ; chromatic dispersion max
        dgd_avg                      = FLOAT                            ; differential group delay avg
        dgd_min                      = FLOAT                            ; differential group delay min
        dgd_max                      = FLOAT                            ; differential group delay max
        sopmd_avg                    = FLOAT                            ; second order polarization mode dispersion avg
        sopmd_min                    = FLOAT                            ; second order polarization mode dispersion min
        sopmd_max                    = FLOAT                            ; second order polarization mode dispersion max
        pdl_avg                      = FLOAT                            ; polarization dependent loss avg
        pdl_min                      = FLOAT                            ; polarization dependent loss min
        pdl_max                      = FLOAT                            ; polarization dependent loss max
        osnr_avg                     = FLOAT                            ; optical signal to noise ratio avg
        osnr_min                     = FLOAT                            ; optical signal to noise ratio min
        osnr_max                     = FLOAT                            ; optical signal to noise ratio max
        esnr_avg                     = FLOAT                            ; electrical signal to noise ratio avg
        esnr_min                     = FLOAT                            ; electrical signal to noise ratio min
        esnr_max                     = FLOAT                            ; electrical signal to noise ratio max
        cfo_avg                      = FLOAT                            ; carrier frequency offset avg
        cfo_min                      = FLOAT                            ; carrier frequency offset min
        cfo_max                      = FLOAT                            ; carrier frequency offset max
        soproc_avg                   = FLOAT                            ; state of polarization rate of change avg
        soproc_min                   = FLOAT                            ; state of polarization rate of change min
        soproc_max                   = FLOAT                            ; state of polarization rate of change max
        tx_power_avg                 = FLOAT                            ; tx output power avg
        tx_power_min                 = FLOAT                            ; tx output power min
        tx_power_max                 = FLOAT                            ; tx output power max
        rx_tot_power_avg             = FLOAT                            ; rx total power avg
        rx_tot_power_min             = FLOAT                            ; rx total power min
        rx_tot_power_max             = FLOAT                            ; rx total power max
        rx_sig_power_avg             = FLOAT                            ; rx signal power avg
        rx_sig_power_min             = FLOAT                            ; rx signal power min
        rx_sig_power_max             = FLOAT                            ; rx signal power max
        ========================================================================
        """
        trans_pm = dict()
        PM_dict = self.get_pm_all()
        trans_pm['prefec_ber_avg'] = PM_dict['preFEC_BER_avg']
        trans_pm['prefec_ber_min'] = PM_dict['preFEC_BER_min']
        trans_pm['prefec_ber_max'] = PM_dict['preFEC_BER_max']
        trans_pm['uncorr_frames_avg'] = PM_dict['preFEC_uncorr_frame_ratio_avg']
        trans_pm['uncorr_frames_min'] = PM_dict['preFEC_uncorr_frame_ratio_min']
        trans_pm['uncorr_frames_max'] = PM_dict['preFEC_uncorr_frame_ratio_max']
        trans_pm['cd_avg'] = PM_dict['rx_cd_avg']
        trans_pm['cd_min'] = PM_dict['rx_cd_min']
        trans_pm['cd_max'] = PM_dict['rx_cd_max']
        trans_pm['dgd_avg'] = PM_dict['rx_dgd_avg']
        trans_pm['dgd_min'] = PM_dict['rx_dgd_min']
        trans_pm['dgd_max'] = PM_dict['rx_dgd_max']
        trans_pm['sopmd_avg'] = PM_dict['rx_sopmd_avg']
        trans_pm['sopmd_min'] = PM_dict['rx_sopmd_min']
        trans_pm['sopmd_max'] = PM_dict['rx_sopmd_max']
        trans_pm['pdl_avg'] = PM_dict['rx_pdl_avg']
        trans_pm['pdl_min'] = PM_dict['rx_pdl_min']
        trans_pm['pdl_max'] = PM_dict['rx_pdl_max']
        trans_pm['osnr_avg'] = PM_dict['rx_osnr_avg']
        trans_pm['osnr_min'] = PM_dict['rx_osnr_min']
        trans_pm['osnr_max'] = PM_dict['rx_osnr_max']
        trans_pm['esnr_avg'] = PM_dict['rx_esnr_avg']
        trans_pm['esnr_min'] = PM_dict['rx_esnr_min']
        trans_pm['esnr_max'] = PM_dict['rx_esnr_max']
        trans_pm['cfo_avg'] = PM_dict['rx_cfo_avg']
        trans_pm['cfo_min'] = PM_dict['rx_cfo_min']
        trans_pm['cfo_max'] = PM_dict['rx_cfo_max']
        trans_pm['evm_avg'] = PM_dict['rx_evm_avg']
        trans_pm['evm_min'] = PM_dict['rx_evm_min']
        trans_pm['evm_max'] = PM_dict['rx_evm_max']
        trans_pm['soproc_avg'] = PM_dict['rx_soproc_avg']
        trans_pm['soproc_min'] = PM_dict['rx_soproc_min']
        trans_pm['soproc_max'] = PM_dict['rx_soproc_max']
        trans_pm['tx_power_avg'] = PM_dict['tx_power_avg']
        trans_pm['tx_power_min'] = PM_dict['tx_power_min']
        trans_pm['tx_power_max'] = PM_dict['tx_power_max']
        trans_pm['rx_tot_power_avg'] = PM_dict['rx_power_avg']
        trans_pm['rx_tot_power_min'] = PM_dict['rx_power_min']
        trans_pm['rx_tot_power_max'] = PM_dict['rx_power_max']
        trans_pm['rx_sig_power_avg'] = PM_dict['rx_sigpwr_avg']
        trans_pm['rx_sig_power_min'] = PM_dict['rx_sigpwr_min']
        trans_pm['rx_sig_power_max'] = PM_dict['rx_sigpwr_max']
        return trans_pm
