import pytest
from raiblocks.accounts import xrb_encode, xrb_decode


XRB_ENCODE_TESTS = [
    ('', ''),
    ('hello', 'f3kpru5h'),
    ('okay', 'fxop4ya='),
]
XRB_DECODE_TESTS = [(encoded, decoded) for decoded, encoded in XRB_ENCODE_TESTS]

@pytest.mark.parametrize('value,expected', XRB_ENCODE_TESTS)
def test_xrb_encode(value, expected):
    assert xrb_encode(value) == expected


@pytest.mark.parametrize('value,expected', XRB_DECODE_TESTS)
def test_xrb_decode(value, expected):
    assert xrb_decode(value) == expected
