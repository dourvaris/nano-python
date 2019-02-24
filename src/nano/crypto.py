import string
import struct
from base64 import b32encode, b32decode

from pyblake2 import blake2b

from . import ed25519_blake2

maketrans = hasattr(bytes, 'maketrans') and bytes.maketrans or string.maketrans
B32_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
XRB_ALPHABET = b'13456789abcdefghijkmnopqrstuwxyz'
XRB_ENCODE_TRANS = maketrans(B32_ALPHABET, XRB_ALPHABET)
XRB_DECODE_TRANS = maketrans(XRB_ALPHABET, B32_ALPHABET)


def address_checksum(address):
    """
    Returns the checksum in bytes for an address in bytes
    """
    address_bytes = address
    h = blake2b(digest_size=5)
    h.update(address_bytes)
    checksum = bytearray(h.digest())
    checksum.reverse()
    return checksum


def private_to_public_key(private_key):
    """
    Returns the public key for a private key

    :param private_key: private key (in bytes) to get public key for
    :type private_key: bytes
    """
    return ed25519_blake2.publickey_unsafe(private_key)


def keypair_from_seed(seed, index=0):
    """
    Generates a deterministic keypair from `seed` based on `index`

    :param seed: bytes value of seed
    :type seed: bytes

    :param index: offset from seed
    :type index: int

    :return: dict of the form: {
        'private': private_key
        'public': public_key
    }
    """

    h = blake2b(digest_size=32)
    h.update(seed + struct.pack(">L", index))
    priv_key = h.digest()
    pub_key = private_to_public_key(priv_key)
    return {
        'private': priv_key,
        'public': pub_key,
    }


def b32xrb_encode(value):
    """
    Encodes bytes to xrb encoding which uses the base32 algorithm
    with a custom alphabet: '13456789abcdefghijkmnopqrstuwxyz'

    :param value: the value to encode
    :type: bytes

    :return: encoded value
    :rtype: bytes

    >>> b32xrb_encode(b'deadbeef')
    b'ejkp4s54eokpe==='
    """
    return b32encode(value).translate(XRB_ENCODE_TRANS)


def b32xrb_decode(value):
    """
    Decodes a value in xrb encoding to bytes using base32 algorithm
    with a custom alphabet: '13456789abcdefghijkmnopqrstuwxyz'

    :param value: the value to decode
    :type: bytes

    :return: decoded value
    :rtype: bytes

    >>> b32xrb_decode(b'fxop4ya=')
    b'okay'
    """
    return b32decode(value.translate(XRB_DECODE_TRANS))


def verify_signature(message, signature, public_key):
    """
    Verifies `signature` is correct for a `message` signed with `public_key`

    :param message: message to check
    :type message: bytes

    :param signature: signature to check
    :type signature: bytes

    :param public_key: public_key to check
    :type public_key: bytes

    :return: True if valid, False otherwise
    :rtype: bool
    """

    try:
        ed25519_blake2.checkvalid(signature, message, public_key)
    except ed25519_blake2.SignatureMismatch:
        return False
    return True


def sign_message(message, private_key, public_key=None):
    """
    Signs a `message` using `private_key` and `public_key`

    .. warning:: Not safe to use with secret keys or secret data. See module
                 docstring.  This function should be used for testing only.

    :param message: the message to sign
    :type message: bytes

    :param private_key: private key used to sign message
    :type private_key: bytes

    :param public_key: public key used to sign message
    :type public_key: bytes

    :return: the signature of the signed message
    :rtype: bytes
    """

    if public_key is None:
        public_key = private_to_public_key(private_key)

    return ed25519_blake2.signature_unsafe(message, private_key, public_key)
