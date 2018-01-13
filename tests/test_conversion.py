import pytest
from decimal import Decimal
import raiblocks.conversion
from raiblocks.conversion import converter
from raiblocks.conversion import (
    XRB_to_Grai, XRB_to_Gxrb, XRB_to_Mrai, XRB_to_Mxrb, XRB_to_krai,
    XRB_to_kxrb, XRB_to_mrai, XRB_to_mxrb, XRB_to_rai, XRB_to_raw, XRB_to_urai,
    XRB_to_uxrb, XRB_to_xrb,
    raw_to_Grai, raw_to_Gxrb, raw_to_Mrai, raw_to_Mxrb, raw_to_XRB, raw_to_krai,
    raw_to_kxrb, raw_to_mrai, raw_to_mxrb, raw_to_rai, raw_to_urai, raw_to_uxrb,
    raw_to_xrb,
)

@pytest.mark.parametrize('value,from_unit,expected,to_unit', [
(
    Decimal('1'), 'XRB',
    Decimal('1'), 'XRB',
),
(
    Decimal('1'), 'XRB',
    Decimal('0.001'), 'Gxrb',
),
(
    Decimal('1'), 'XRB',
    Decimal('1'), 'Mxrb',
),
(
    Decimal('1'), 'XRB',
    Decimal('1000'), 'kxrb',
),
(
    Decimal('1'), 'XRB',
    Decimal('1000000'), 'xrb',
),
(
    Decimal('1'), 'XRB',
    Decimal('1000000000'), 'mxrb',
),
(
    Decimal('1'), 'XRB',
    Decimal('1000000000000'), 'uxrb',
),
(
    Decimal('340282366920938463463374607431768211455'), 'raw',
    Decimal('340282366.9209384634633746074'), 'XRB',
),
(   # is <long>
    340282366920938463463374607431768211455, 'raw',
    Decimal('340282366.9209384634633746074'), 'XRB',
),
(
    Decimal('-1'), 'XRB',
    Decimal('-1'), 'XRB',
),
(
    Decimal('-1'), 'XRB',
    Decimal('-1000000'), 'xrb',
),
(
    Decimal('3.142'), 'XRB',
    Decimal('3142000'), 'xrb',
),
(
    Decimal('-3.142'), 'XRB',
    Decimal('-3142000'), 'xrb',
),
(
    Decimal('-3142000'), 'raw',
    Decimal('-3142000'), 'raw',
),
])
def test_convert(value, from_unit, expected, to_unit):
    result = converter(value, from_unit, to_unit)
    assert result == expected

    # test the dynamically generated function here
    func_name = '%s_to_%s' % (from_unit, to_unit)
    if from_unit == to_unit:
        with pytest.raises(AttributeError):
            getattr(raiblocks.conversion, func_name)
    else:
        assert getattr(raiblocks.conversion, func_name)(value) == expected


@pytest.mark.parametrize('value,from_unit,to_unit', [
    (1, 'badunit', 'XRB'),
    (1, 'XRB', 'badunit'),
    ('string', 'XRB', 'XRB'),
    (1.4, 'XRB', 'XRB'),
])
def test_invalid_convert(value, from_unit, to_unit):
    with pytest.raises(ValueError):
        converter(value, from_unit=from_unit, to_unit=to_unit)

