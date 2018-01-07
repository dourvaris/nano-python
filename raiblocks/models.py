"Models for raiblocks"


class Account(str):

    def __new__(cls, value):
        # FIXME(dan): this is not perfect yet - still need to check by hash
        if not len(value) == 64:
            raise ValueError('invalid account, not 64 characters')

        lowercase = value.lower()
        prefix, rest = lowercase[:4], lowercase[4:]

        if prefix != 'xrb_':
            raise ValueError('invalid account, doesnt start with xrb_')

        for char in rest:
            if char not in 'abcdefghijklmnopqrstuvwxyz0123456789':
                raise ValueError('invalid character in account: %r' % char)

        return super(Account, cls).__new__(cls, value)


class Hash(str):
    size = 64

    def __new__(cls, value):
        if not len(value) == cls.size:
            raise ValueError('invalid wallet id, not 64 characters')

        for char in value.upper():
            if char not in '0123456789ABCDEF':
                raise ValueError('invalid character in wallet id: %r' % char)

        return super(Hash, cls).__new__(cls, value)


class Seed(Hash):
    pass


class Wallet(Hash):
    pass


class PrivateKey(Hash):
    pass


class PublicKey(Hash):
    pass


class Block(Hash):
    pass


class Seed(Hash):
    pass

class Work(Hash):
    size = 16
