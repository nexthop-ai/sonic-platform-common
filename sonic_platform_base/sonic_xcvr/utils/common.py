"""
    common.py

    Common helper functions shared across transceiver APIs.
"""


def get_F16(value):
    '''
    This function converts raw data to "F16" format defined in cmis.
    '''
    if value is None or value < 0:
        return None
    scale_exponent = (value >> 11) & 0x1f
    mantissa = value & 0x7ff
    result = mantissa*10**(scale_exponent-24)
    return result


def set_F16(value):
    '''
    This function converts a value to raw data in "F16" format defined in cmis.
    Returns None if the value is negative or too large to represent.
    '''
    if value is None or value < 0:
        return None
    if value == 0:
        return 0
    # Pick the smallest exponent that keeps the mantissa in range, which
    # maximises mantissa precision.
    for scale_exponent in range(0, 0x1f + 1):
        mantissa = round(value / 10**(scale_exponent-24))
        if mantissa <= 0x7ff:
            return ((scale_exponent & 0x1f) << 11) | (mantissa & 0x7ff)
    return None
