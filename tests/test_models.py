import pytest

from raiblocks.models import Account, Wallet


class TestAccount(object):
    @pytest.mark.parametrize('value', [
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000',
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi11111111',
        'xrb_25355tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi11111111',
        'XRB_25355tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi11111111',
        'XRB_CAPITALS111pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi11111111',
        'xrb_CAPITALS111pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi11111111',
    ])
    def test_valid_account(self, value):
        assert Account(value) == value

    @pytest.mark.parametrize('value', [
        # TODO(dan): add tests for validity of the string based on hash
        '',
        ' ' * 60,
        'xrp_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000',
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi0000000',
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi000000001',
        'xrb_' + 60 * '!',
        'xrb_' + 60 * '$',
        'xrb_' + u'\xb4' + 59 * u'1',
        'xrb_' + 60 * '$',
    ])
    def test_invalid_account(self, value):
        with pytest.raises(ValueError):
            Account(value)


class TestWallet(object):
    @pytest.mark.parametrize('value', [
        '000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F',
        '000d1baec8ec208142c99059b393051bac8380f9b5a2e6b2489a277d81789f3f',
        '1BAEC8EC208142C99059B393051BAC8380000DF9B5A2E6B2489A277D81789F3F',
    ])
    def test_valid_wallet(self, value):
        assert Wallet(value) == value

    @pytest.mark.parametrize('value', [
        '',
        ' ' * 64,
        'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ',
    ])
    def test_invalid_wallet(self, value):
        with pytest.raises(ValueError):
            Wallet(value)
