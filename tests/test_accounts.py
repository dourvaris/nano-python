import pytest
from nano.accounts import (
    bytes_to_xrb, xrb_to_bytes, hex_to_xrb, xrb_to_hex)


XRB_BYTES_ENCODE_TESTS = [
    (b'', b''),
    (b'hello', b'f3kpru5h'),
    (b'okay', b'fxop4ya='),
    (b'deadbeef', b'ejkp4s54eokpe==='),
]
XRB_BYTES_DECODE_TESTS = [
    (encoded, decoded) for decoded, encoded in XRB_BYTES_ENCODE_TESTS]

@pytest.mark.parametrize('value,expected', XRB_BYTES_ENCODE_TESTS)
def test_bytes_to_xrb(value, expected):
    assert bytes_to_xrb(value) == expected


@pytest.mark.parametrize('value,expected', XRB_BYTES_DECODE_TESTS)
def test_xrb_to_bytes(value, expected):
    assert xrb_to_bytes(value) == expected


XRB_HEX_ENCODE_TESTS = [
    (b'', b''),
    (b'deadbeef', b'utpuxur='),
]
XRB_HEX_DECODE_TESTS = [
    (encoded, decoded) for decoded, encoded in XRB_HEX_ENCODE_TESTS]

@pytest.mark.parametrize('value,expected', XRB_HEX_ENCODE_TESTS)
def test_hex_to_xrb(value, expected):
    assert hex_to_xrb(value) == expected


@pytest.mark.parametrize('value,expected', XRB_HEX_DECODE_TESTS)
def test_xrb_to_hex(value, expected):
    assert xrb_to_hex(value) == expected
