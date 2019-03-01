from binascii import hexlify, unhexlify

import pytest

from nano.accounts import (
    public_key_to_xrb_address,
    xrb_address_to_public_key,
    generate_account,
)
from nano.crypto import private_to_public_key

ACCOUNT_TESTS = [
    {
        'address': (
            'xrb_3n4fgjgiisyoc1zjen5o1jq3554u' '3t8htjsr6k5yibza3p9yp3kfpgeycnxj'
        ),
        'public_hex': (
            'D04D745D0867D5503F165075046E118C' '5B0E8CFD47382487E827E80D8FEB064D'
        ),
    },
    {
        'address': (
            'xrb_34147sxe87n51z174urzg8cbboda' 'hrf7gzuyqbshtkw3ueqgme883mecq9wn'
        ),
        'public_hex': (
            '88022E7AC3168307C0516F1F719494D5' '687E1A577F7EBA72FD4B81DB2EE9B0C6'
        ),
    },
]


@pytest.mark.parametrize('data', ACCOUNT_TESTS)
def test_xrb_address_to_public_key(data):
    public_key = xrb_address_to_public_key(data['address'])
    assert public_key == unhexlify(data['public_hex'])


@pytest.mark.parametrize(
    'address,error_msg',
    [
        ('xrb_34147sxe87n51z174urzg8cbbodahrf7gzuyqbshtkw3ueqgme883mecq9wn', ''),
        (
            'xrb_34147sxe87n51z174urzg8cbbodahrf7gzuyqbshtkw3ueqgme883mecq9w3',
            'invalid checksum',
        ),
        (
            'xrp_34147sxe87n51z174urzg8cbbodahrf7gzuyqbshtkw3ueqgme883mecq9w3',
            'does not start with xrb_',
        ),
        (
            'xrb_34147sxe87n51z174urzg8cbbodahrf7gzuyqbshtkw3ueqgme883mecq9wn3',
            'must be 64 chars',
        ),
        (
            'xrb_34147sxe87n51z174urzg8cbbodahrf7gzuyqbshtkw3ueqgme883mecq9w',
            'must be 64 chars',
        ),
    ],
)
def test_invalid_xrb_addresses(address, error_msg):
    if not error_msg:  # test the valid case is working
        assert xrb_address_to_public_key(address) == (
            unhexlify(
                '88022E7AC3168307C0516F1F719494D5' '687E1A577F7EBA72FD4B81DB2EE9B0C6'
            )
        )
        return

    with pytest.raises(ValueError) as e_info:
        xrb_address_to_public_key(address)

    assert e_info.match(error_msg)


@pytest.mark.parametrize('data', ACCOUNT_TESTS)
def test_public_key_to_xrb_address(data):
    address = public_key_to_xrb_address(unhexlify(data['public_hex']))
    assert address == data['address']


@pytest.mark.parametrize(
    'public_key,error_msg',
    [
        (b'00000000000000000000000000000000', ''),
        (b'000000000000000000000000000000000', 'must be 32 chars'),
        (b'0000000000000000000000000000000', 'must be 32 chars'),
    ],
)
def test_invalid_private_keys(public_key, error_msg):
    if not error_msg:  # test the valid case is working
        assert public_key_to_xrb_address(public_key) == (
            'xrb_1e3i81r51e3i81r51e3i81r51e3i' '81r51e3i81r51e3i81r51e3imxssakuq'
        )
        return

    with pytest.raises(ValueError) as e_info:
        public_key_to_xrb_address(public_key)

    assert e_info.match(error_msg)


def test_generate_account_from_seed():
    account = generate_account(seed=unhexlify(64 * '0'))

    public_key = unhexlify(
        'c008b814a7d269a1fa3c6528b19201a2' '4d797912db9996ff02a1ff356e45552b'
    )
    private_key = unhexlify(
        '9f0e444c69f77a49bd0be89db92c38fe7' '13e0963165cca12faf5712d7657120f'
    )

    assert account == {
        'address': (
            u'xrb_3i1aq1cchnmbn9x5rsbap8b15akf' 'h7wj7pwskuzi7ahz8oq6cobd99d4r3b7'
        ),
        'public_key_bytes': public_key,
        'public_key_hex': hexlify(public_key),
        'private_key_bytes': private_key,
        'private_key_hex': hexlify(private_key),
    }


def test_generate_account_random():
    seen = set()
    for i in range(5):
        account = generate_account()
        assert account['address'] not in seen
        seen.add(account['address'])

        assert (
            private_to_public_key(account['private_key_bytes'])
            == account['public_key_bytes']
        )
        assert (
            public_key_to_xrb_address(account['public_key_bytes']) == account['address']
        )
