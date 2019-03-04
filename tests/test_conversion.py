from decimal import Decimal

import pytest

from nano.conversion import convert


@pytest.mark.parametrize(
    'value,from_unit,expected,to_unit',
    [
        (Decimal('1'), 'XRB', Decimal('1'), 'NANO'),
        (Decimal('1'), 'XRB', Decimal('0.001'), 'Gxrb'),
        (Decimal('1'), 'NANO', Decimal('1'), 'Mxrb'),
        (Decimal('1'), 'XRB', Decimal('1000'), 'kxrb'),
        (Decimal('1'), 'XRB', Decimal('1000000'), 'xrb'),
        (Decimal('1'), 'XRB', Decimal('1000000000'), 'mxrb'),
        (Decimal('1'), 'XRB', Decimal('1000000000000'), 'urai'),
        (
            Decimal('340282366920938463463374607431768211455'),
            'raw',
            Decimal('340282366.9209384634633746074'),
            'XRB',
        ),
        (  # is <long>
            340282366920938463463374607431768211455,
            'raw',
            Decimal('340282366.9209384634633746074'),
            'XRB',
        ),
        (Decimal('-1'), 'XRB', Decimal('-1'), 'Mrai'),
        (Decimal('-1'), 'NANO', Decimal('-1000000'), 'xrb'),
        (Decimal('3.142'), 'XRB', Decimal('3142000'), 'xrb'),
        (Decimal('-3.142'), 'XRB', Decimal('-3142000'), 'xrb'),
        (Decimal('-3142000'), 'raw', Decimal('-3142000'), 'raw'),
    ],
)
def test_convert(value, from_unit, expected, to_unit):
    result = convert(value, from_unit, to_unit)
    assert result == expected


@pytest.mark.parametrize(
    'value,from_unit,to_unit',
    [
        (1, 'badunit', 'XRB'),
        (1, 'XRB', 'badunit'),
        ('string', 'XRB', 'XRB'),
        (1.4, 'XRB', 'XRB'),
    ],
)
def test_invalid_convert(value, from_unit, to_unit):
    with pytest.raises(ValueError):
        convert(value, from_unit=from_unit, to_unit=to_unit)
