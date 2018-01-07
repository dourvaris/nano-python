

class Account(str):
    def __new__(cls, value):
        value = value.lower()

        # FIXME(dan): this is not perfect yet - still need to check by hash

        if not len(value) == 64:
            raise ValueError('invalid account, not 64 characters')

        prefix, rest = value[:4], value[4:]

        if prefix != 'xrb_':
            raise ValueError('invalid account, doesnt start with xrb_')

        for char in rest:
            if char not in 'abcdefghijklmnopqrstuvwxyz0123456789':
                raise ValueError('invalid character in account: %r' % char)

        return super(Account, cls).__new__(cls, value)
