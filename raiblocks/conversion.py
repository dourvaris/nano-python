from decimal import Decimal
from functools import partial
from itertools import permutations

"""
Conversion tools for converting xrb


Gxrb = 1000000000000000000000000000000000raw, 10^33
Mxrb = 1000000000000000000000000000000raw, 10^30
kxrb = 1000000000000000000000000000raw, 10^27
xrb  = 1000000000000000000000000raw, 10^24
mxrb = 1000000000000000000000raw, 10^21
uxrb = 1000000000000000000raw, 10^18

1 Mxrb used to be also called 1 Mrai
1 xrb is 10^24 raw
1 raw is the smallest possible division

Mrai are XRB
1rai = 1000krai = 1,000,000mrai = 0,000001 XRB

"""

BASE_UNIT = 'raw'
UNIT_NAMES = ['xrb', 'rai']
UNITS_TO_RAW = {
    BASE_UNIT: 1
}
CONVERTERS = {}


def _populate_units():
    # populate the existing units, eg krai, Mrai, Mxrb etc.
    for name in UNIT_NAMES:
        for i, prefix in enumerate(['G', 'M', 'k', '', 'm', 'u']):
            in_raw = 10 ** (33 - (i * 3))
            unit_name = prefix + name
            UNITS_TO_RAW[unit_name] = Decimal(in_raw)

    # special case for XRB
    UNITS_TO_RAW['XRB'] = UNITS_TO_RAW['Mxrb']


def converter(value, from_unit, to_unit):
    """
    Converts a value from `from_unit` units to `to_unit` units

    :param value: value to convert
    :param from_unit: unit to convert from
    :param to_unit: unit to convert to

    >>> converter(value='1.5', from_unit='xrb', to_unit='krai')

    """

    if isinstance(value, float):
        raise ValueError(
            "float values can lead to unexpected precision loss, please use a"
            " Decimal or string eg."
            " converter('%s', %r, %r)" % (value, from_unit, to_unit)
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


def _register_converter_functions():
    """ Builds and registers functions for all conversions possible """

    for from_unit, to_unit in permutations(UNITS_TO_RAW, 2):
        func_name = '%s_to_%s' % (from_unit, to_unit)

        converter_func = partial(
            converter, from_unit=from_unit, to_unit=to_unit)

        example_value = '123456'
        if to_unit == 'raw':
            example_value = '0.00000123456'
        if from_unit == 'raw':
            example_value = '12345678900000000000000000'

        docstring = '''
            Convert {from_unit} to {to_unit}

            >>> {func_name}({value})
            {result}
            '''.format(
                from_unit=from_unit,
                to_unit=to_unit,
                func_name=func_name,
                value=example_value,
                result=repr(converter_func(example_value))
            )
        converter_func.__doc__ = docstring
        converter_func.__name__ = func_name
        globals()[func_name] = converter_func


_populate_units()
_register_converter_functions()
