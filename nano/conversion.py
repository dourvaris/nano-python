"""
Conversion tools for converting Nano units
Units source: https://github.com/nanocurrency/nano-node/wiki/Distribution,-Mining-and-Units


Gnano/Gxrb/Grai = 1000000000000000000000000000000000raw, 10^33

Mnano/Mxrb/Mrai = 1000000000000000000000000000000raw, 10^30

knano/kxrb/krai = 1000000000000000000000000000raw, 10^27

nano/xrb/rai  = 1000000000000000000000000raw, 10^24

mnano/mxrb/mrai = 1000000000000000000000raw, 10^21

unano/uxrb/urai = 1000000000000000000raw, 10^18

1 raw is the smallest possible division
Mnano used to be called Mxrb or Mrai
1 nano (formerly xrb or rai) is 10^24 raw
Mnano is also called NANO, or in the past XRB

"""

from decimal import Decimal

BASE_UNIT = 'raw'
UNIT_NAMES = ['xrb', 'rai', 'nano']
UNITS_TO_RAW = {
    BASE_UNIT: Decimal(1)
}


def _populate_units():
    # populate the existing units, eg krai, Mrai, Mxrb, Gnano etc.
    for name in UNIT_NAMES:
        for i, prefix in enumerate(['G', 'M', 'k', '', 'm', 'u']):
            in_raw = 10 ** (33 - (i * 3))
            unit_name = prefix + name
            UNITS_TO_RAW[unit_name] = Decimal(in_raw)

    # special case for XRB
    UNITS_TO_RAW['XRB'] = UNITS_TO_RAW['Mnano']
    UNITS_TO_RAW['NANO'] = UNITS_TO_RAW['Mnano']


def convert(value, from_unit, to_unit):
    """
    Converts a value from `from_unit` units to `to_unit` units

    :param value: value to convert
    :type value: int or str or decimal.Decimal

    :param from_unit: unit to convert from
    :type from_unit: str

    :param to_unit: unit to convert to
    :type to_unit: str

    >>> convert(value='1.5', from_unit='xrb', to_unit='krai')
    Decimal('0.0015')
    """

    if isinstance(value, float):
        raise ValueError(
            "float values can lead to unexpected precision loss, please use a"
            " Decimal or string eg."
            " convert('%s', %r, %r)" % (value, from_unit, to_unit)
        )

    if from_unit not in UNITS_TO_RAW:
        raise ValueError('unknown unit: %r' % from_unit)

    if to_unit not in UNITS_TO_RAW:
        raise ValueError('unknown unit: %r' % to_unit)

    try:
        value = Decimal(value)
    except Exception:
        raise ValueError('not a number: %r' % value)

    from_value_in_base = UNITS_TO_RAW[from_unit]
    to_value_in_base = UNITS_TO_RAW[to_unit]

    result = value * (from_value_in_base / to_value_in_base)

    return result.normalize()


_populate_units()
