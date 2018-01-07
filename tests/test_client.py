import json
import pytest
import requests
import requests_mock

from raiblocks.client import Client
from conftest import MockRPCMatchException, load_mock_rpc_tests


mock_rpc_tests = load_mock_rpc_tests()


@pytest.fixture
def client(mock_rpc_session):
    return Client(host='mock://localhost:7076', session=mock_rpc_session)


class TestClient(object):

    @pytest.mark.parametrize('args', [
        {},
        {'host': 'http://localhost:7076/'},
        {'host': 'http://localhost:7076'},
    ])
    def test_create(self, args):
        assert Client(**args)

    def test_call_valid_action(self, client):
        assert client.call('version') == {
            "rpc_version": "1",
            "store_version": "10",
            "node_vendor": "RaiBlocks 9.0"
        }

    def test_call_invalid_action(self, client):

        with pytest.raises(MockRPCMatchException):
            assert client.call('versions')

    @pytest.mark.parametrize('action,test', [
        (action, test)
        for action, tests in mock_rpc_tests.items()
        for test in tests
    ])
    def test_rpc_methods(self, client, action, test):
        try:
            method = getattr(client, action)
        except AttributeError:
            pytest.xfail("`%s` not yet implemented" % action)

        if 'func' not in test:
            pytest.skip("missing functional test")

        functest = test['func']
        args = functest.get('args') or {}

        if 'exception' in functest:
            with pytest.raises(eval(functest['exception'])):
                method(**args)
        elif 'result' in functest:
            result = method(**args)
            assert client.session.adapter.last_request.json() == test['request']

            expected = functest['result']
            if result != expected:
                print('result:')
                print(json.dumps(result, indent=2, sort_keys=True))
                print('expected:')
                print(json.dumps(expected, indent=2, sort_keys=True))
            assert result == expected
        else:
            # valid formats:
            # {
            #     "args": {"x": 10, "y": 5},
            #     "result": 2
            # }
            # {
            #     "args": {"x": 1, "y": 0},
            #     "exception": "ZeroDivisionError"
            # }
            raise Exception("invalid test format: %s" % json.dumps(functest))
