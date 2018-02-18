import pytest
from binascii import unhexlify
from nano.crypto import (
    b32xrb_encode, b32xrb_decode, address_checksum, private_to_public_key,
    keypair_from_seed, verify_signature, sign_message
)


SIGNING_TESTS = [
    {
        'private_key': unhexlify('A1A7DF26F28DBCC9AB2FF66431473C5F'
                                 'C7F6DD48CAC1485CD45F3F9D82616802'),
        'public_key': unhexlify('8A3E229B28FFC19DE27C2FD9AFBB6BA'
                                '8723E7E267B87AA690854AB01543E9D20'),
        'message': unhexlify('5904FC0108F37D30AD57AF9A56F54354'
                             '2476425E473F3C0AFC8D44348BDA48C0'),
        'signature': unhexlify('025CA216857868E2094C246104ADBDC8'
                               '2BC8ACE2C658AB4A68601BA0636187A7'
                               '474AFBB94FDDD05868BA78D7A1C02D3E'
                               '56860BE529539EEBCE810C9D1603540F'),
    }
]


B32XRB_TESTS = [
    (b'', b''),
    (b'hello', b'f3kpru5h'),
    (b'okay', b'fxop4ya='),
    (b'deadbeef', b'ejkp4s54eokpe==='),
]


@pytest.mark.parametrize('decoded,encoded', B32XRB_TESTS)
def test_b32xrb_encode(decoded, encoded):
    result = b32xrb_encode(decoded)
    assert result == encoded


@pytest.mark.parametrize('decoded, encoded', B32XRB_TESTS)
def test_b32xrb_decode(decoded, encoded):
    result = b32xrb_decode(encoded)
    assert result == decoded


@pytest.mark.parametrize('private_key,public_key', [
    (
        unhexlify('9f0e444c69f77a49bd0be89db92c38fe'
                  '713e0963165cca12faf5712d7657120f'),
        unhexlify('c008b814a7d269a1fa3c6528b19201a2'
                  '4d797912db9996ff02a1ff356e45552b'),
    )
])
def test_private_to_public_key(private_key, public_key):
    result = private_to_public_key(private_key)
    assert result == public_key


@pytest.mark.parametrize('value,expected', [
    (b'', b'.\'\xc5d}'),
    (b'\x01$', b'\xa3\x88\xe8#\xe6'),
])
def test_address_checksum(value, expected):
    assert address_checksum(value) == expected

@pytest.mark.parametrize('args,expected', [
    (
        (unhexlify(b'0' * 64),),
        {
            'private': unhexlify('9f0e444c69f77a49bd0be89db92c38fe'
                                 '713e0963165cca12faf5712d7657120f'),
            'public': unhexlify('c008b814a7d269a1fa3c6528b19201a24'
                                'd797912db9996ff02a1ff356e45552b'),
        }
    ),
    (
        (unhexlify(b'0' * 64), 0),
        {
            'private': unhexlify('9f0e444c69f77a49bd0be89db92c38fe'
                                 '713e0963165cca12faf5712d7657120f'),
            'public': unhexlify('c008b814a7d269a1fa3c6528b19201a24'
                                'd797912db9996ff02a1ff356e45552b'),
        }
    ),
    (
        (unhexlify(b'0' * 64), 1),
        {
            'private': unhexlify('b73b723bf7bd042b66ad3332718ba98d'
                                 'e7312f95ed3d05a130c9204552a7afff'),
            'public': unhexlify('e30d22b7935bcc25412fc07427391ab4c'
                                '98a4ad68baa733300d23d82c9d20ad3'),
        }
    ),
    (
        (unhexlify(b'1' * 64),),
        {
            'private': unhexlify('DBD5DF42B3D4120A9E8F6D3B2EEDCDC2'
                                 '1AD27CF76E95978564F66F44E0240184'),
            'public': unhexlify('2791D5A1697D454448F9EEABA2A336E52'
                                '2D5767E570B326278F5532194F642C8'),
        }
    ),
    (
        (unhexlify(b'1' * 64), 0),
        {
            'private': unhexlify('DBD5DF42B3D4120A9E8F6D3B2EEDCDC2'
                                 '1AD27CF76E95978564F66F44E0240184'),
            'public': unhexlify('2791D5A1697D454448F9EEABA2A336E52'
                                '2D5767E570B326278F5532194F642C8'),
        }
    ),
    (
        (unhexlify(b'1' * 64), 1),
        {
            'private': unhexlify('4A6E3512ACBB38A3D6BCF53D5452E11F'
                                 '6B34C30D0405139E3328FD7A63E2D612'),
            'public': unhexlify('E04BC3CAEDAA1787E9373A105453160E4'
                                'B6BEDFE1782A0DBA0C98A89D435DD27'),
        }
    ),
])
def test_keypair_from_seed(args, expected):
    result = keypair_from_seed(*args)
    assert result == expected


@pytest.mark.parametrize('data', SIGNING_TESTS)
def test_verify_signature(data):
    public_key = data['public_key']
    message = data['message']
    signature = data['signature']

    assert verify_signature(message, signature, public_key) == True
    assert verify_signature(message + b'1', signature, public_key) == False


@pytest.mark.parametrize('data', SIGNING_TESTS)
def test_sign_message(data):
    public_key = data['public_key']
    private_key = data['private_key']
    message = data['message']
    expected_signature = data['signature']

    signature = sign_message(message, private_key, public_key)
    assert signature == expected_signature


@pytest.mark.parametrize('message,signature,public_key,error_msg', [
    (b'a message', b'badsig', b'0'*32, 'signature length is wrong'),
    (b'a message', b'0'*64, b'badpubkey', 'public-key length is wrong'),
    (b'a message', b'0'*64, b'0'*32, 'decoding point that is not on curve'),
])
def test_verify_signature_invalid(message, signature, public_key, error_msg):
    with pytest.raises(ValueError) as e_info:
        verify_signature(message, signature, public_key)

    assert e_info.match(error_msg)
