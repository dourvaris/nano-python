"""
Accounts module

``nano.accounts.KNOWN_ACCOUNT_IDS``: dict of account ids => names eg.

>>> KNOWN_ACCOUNT_IDS['xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est']
'Developer Fund'

``nano.accounts.KNOWN_ACCOUNT_NAMES``: dict of names => account ids

>>> KNOWN_ACCOUNT_NAMES['Burn']
'xrb_1111111111111111111111111111111111111111111111111111hifc8npp'

"""

import random
from binascii import hexlify, unhexlify

from .crypto import b32xrb_encode, b32xrb_decode, address_checksum, keypair_from_seed

KNOWN_ACCOUNT_IDS = {
    'xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3': 'Genesis',
    'xrb_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo': 'Landing',
    'xrb_35jjmmmh81kydepzeuf9oec8hzkay7msr6yxagzxpcht7thwa5bus5tomgz9': 'Faucet',
    'xrb_1111111111111111111111111111111111111111111111111111hifc8npp': 'Burn',
    'xrb_3wm37qz19zhei7nzscjcopbrbnnachs4p1gnwo5oroi3qonw6inwgoeuufdp': 'Developer Donations',
    'xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est': 'Developer Fund',
    'xrb_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4': 'Official representative #1',
    'xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou': 'Official representative #2',
    'xrb_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p': 'Official representative #3',
    'xrb_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m': 'Official representative #4',
    'xrb_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k': 'Official representative #5',
    'xrb_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy': 'Official representative #6',
    'xrb_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs': 'Official representative #7',
    'xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1': 'Official representative #8',
    'xrb_3wu7h5in34ntmbiremyxtszx7ufgkceb3jx8orkuncyytcxwzrawuf3dy3sh': 'RaiWalletBot',
    'xrb_16k5pimotz9zehjk795wa4qcx54mtusk8hc5mdsjgy57gnhbj3hj6zaib4ic': 'RaiWalletBot representative',
    'xrb_39ymww61tksoddjh1e43mprw5r8uu1318it9z3agm7e6f96kg4ndqg9tuds4': 'BitGrail Representative 1',
    'xrb_31a51k53fdzam7bhrgi4b67py9o7wp33rec1hi7k6z1wsgh8oagqs7bui9p1': 'BitGrail Representative 2',
    'xrb_3decyj8e1kpzrthikh79x6dwhn8ei81grennibmt43mcm9o8fgxqd8t46whj': 'Mercatox Representative',
    'xrb_369dmjiipkuwar1zxxiuixaqq1kfmyp9rwsttksxdbf8zi3qwit1kxiujpdo': 'RaiBlocks Community',
    'xrb_1niabkx3gbxit5j5yyqcpas71dkffggbr6zpd3heui8rpoocm5xqbdwq44oh': 'KuCoin Representative',
}

KNOWN_ACCOUNT_NAMES = dict(
    (name, account) for account, name in KNOWN_ACCOUNT_IDS.items()
)


def public_key_to_xrb_address(public_key):
    """
    Convert `public_key` (bytes) to an xrb address

    >>> public_key_to_xrb_address(b'00000000000000000000000000000000')
    'xrb_1e3i81r51e3i81r51e3i81r51e3i81r51e3i81r51e3i81r51e3imxssakuq'

    :param public_key: public key in bytes
    :type public_key: bytes

    :return: xrb address
    :rtype: str
    """

    if not len(public_key) == 32:
        raise ValueError('public key must be 32 chars')

    padded = b'000' + public_key
    address = b32xrb_encode(padded)[4:]
    checksum = b32xrb_encode(address_checksum(public_key))
    return 'xrb_' + address.decode('ascii') + checksum.decode('ascii')


def xrb_address_to_public_key(address):
    """
    Convert an xrb address to public key in bytes

    >>> xrb_address_to_public_key('xrb_1e3i81r51e3i81r51e3i81r51e3i'\
                                  '81r51e3i81r51e3i81r51e3imxssakuq')
    b'00000000000000000000000000000000'

    :param address: xrb address
    :type address: bytes

    :return: public key in bytes
    :rtype: bytes

    :raises ValueError:
    """

    address = bytearray(address, 'ascii')

    if not address.startswith(b'xrb_'):
        raise ValueError('address does not start with xrb_: %s' % address)

    if len(address) != 64:
        raise ValueError('address must be 64 chars long: %s' % address)

    address = bytes(address)
    key_b32xrb = b'1111' + address[4:56]
    key_bytes = b32xrb_decode(key_b32xrb)[3:]
    checksum = address[56:]

    if b32xrb_encode(address_checksum(key_bytes)) != checksum:
        raise ValueError('invalid address, invalid checksum: %s' % address)

    return key_bytes


def generate_account(seed=None, index=0):
    """
    Generates an adhoc account and keypair

    >>> account = generate_account(seed=unhexlify('0'*64))
    {'address': u'xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7',
     'private_key_bytes': '\x9f\x0eDLi\xf7zI\xbd\x0b\xe8\x9d\xb9,8\xfeq>\tc\x16\\\xca\x12\xfa\xf5q-vW\x12\x0f',
     'private_key_hex': '9f0e444c69f77a49bd0be89db92c38fe713e0963165cca12faf5712d7657120f',
     'public_key_bytes': '\xc0\x08\xb8\x14\xa7\xd2i\xa1\xfa<e(\xb1\x92\x01\xa2Myy\x12\xdb\x99\x96\xff\x02\xa1\xff5nEU+',
     'public_key_hex': 'c008b814a7d269a1fa3c6528b19201a24d797912db9996ff02a1ff356e45552b'}

    :param seed: the seed in bytes to use to generate the account, if not
                 provided one is generated randomly
    :type seed: bytes

    :param index: the index offset for deterministic account generation
    :type index: int

    :return: dict containing the account address and pub/priv keys in hex/bytes
    :rtype: dict
    """

    if not seed:
        seed = unhexlify(''.join(random.choice('0123456789ABCDEF') for i in range(64)))

    pair = keypair_from_seed(seed, index=index)
    result = {
        'address': public_key_to_xrb_address(pair['public']),
        'private_key_bytes': pair['private'],
        'public_key_bytes': pair['public'],
    }
    result['private_key_hex'] = hexlify(pair['private'])
    result['public_key_hex'] = hexlify(pair['public'])

    return result
