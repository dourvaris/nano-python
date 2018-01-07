import pytest

from raiblocks.models import Account


class TestAccount(object):
    @pytest.mark.parametrize('value', [
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000',
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi11111111',
        'xrb_25355tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi11111111',
    ])
    def test_valid_account(self, value):
        assert Account(value) == value

    @pytest.mark.parametrize('value', [
        # TODO(dan): add tests for validity of the string based on hash
        '',
        ' ' * 60,
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi0000000',
        'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi000000001',
        'xrb_' + 60 * '!',
        'xrb_' + 60 * '$',
        'xrb_' + 60 * u'\xb4',
        'xrb_' + 60 * '$',
    ])
    def test_invalid_account(self, value):
        with pytest.raises(ValueError):
            Account(value)
