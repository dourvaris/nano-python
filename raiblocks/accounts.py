"""
Accounts module

``raiblocks.accounts.KNOWN_ACCOUNT_IDS``: dict of account ids => names eg.

>>> KNOWN_ACCOUNT_IDS['xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est']
'Developer Fund'

``raiblocks.accounts.KNOWN_ACCOUNT_NAMES``: dict of names => account ids

>>> KNOWN_ACCOUNT_NAMES['Burn']
'xrb_1111111111111111111111111111111111111111111111111111hifc8npp'

"""

import six
import string
from binascii import hexlify, unhexlify
from base64 import b32encode, b32decode

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
    (name, account) for account, name in KNOWN_ACCOUNT_IDS.items())

maketrans = bytes.maketrans if hasattr(bytes, 'maketrans') else string.maketrans
B32_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
XRB_ALPHABET = b'13456789abcdefghijkmnopqrstuwxyz'
XRB_ENCODE_TRANS = maketrans(B32_ALPHABET, XRB_ALPHABET)
XRB_DECODE_TRANS = maketrans(XRB_ALPHABET, B32_ALPHABET)


def bytes_to_xrb(value):
    """
    Encodes a hex value to xrb format which uses the base32 algorithm
    with a custom alphabet: '13456789abcdefghijkmnopqrstuwxyz'

    >>> xrb_encode(b'deadbeef')
    b'ejkp4s54eokpe'
    """
    return b32encode(value).translate(XRB_ENCODE_TRANS)


def hex_to_xrb(value):
    """
    Encodes a hex string to xrb format

    >>> xrb_encode(b'deadbeef')
    b'utpuxur'
    """

    return bytes_to_xrb(unhexlify(value))


def xrb_to_bytes(value):
    """
    Encodes an xrb string to bytes

    >>> xrb_encode(b'ejkp4s54eokpe')
    b'deadbeef'
    """
    return b32decode(value.translate(XRB_DECODE_TRANS))

def xrb_to_hex(value):
    """
    Encodes an xrb string to hex

    >>> xrb_encode(b'utpuxur')
    b'deadbeef'
    """
    return hexlify(xrb_to_bytes(value))
