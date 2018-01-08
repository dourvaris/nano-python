import json
import pytest
import requests
import requests_mock

from raiblocks.client import RPCException
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
        """
        Tests should be in the format:

        {
            "args": {"values": [3, 2]},
            "expected": 5,
            "request": {
                "add": [3, 2]
            },
            "response": "5"
        }

        Assuming we want to test a function add(values=[3, 2]) which sends
        a request to the backend with {"add": [3, 2]} and gets a response
        with string "5" and the function returns int 5

        If the response contains an "error" key, it is assumed the function
        must raise an `RPCException` and "expected" is ignored
        """

        try:
            method = getattr(client, action)
        except AttributeError:
            raise Exception("`%s` not yet implemented" % action)
            pytest.xfail("`%s` not yet implemented" % action)

        try:
            args = test.get('args') or {}
            expected = test['expected']
            request = test['request']
            response = test['response']
        except KeyError:
            raise Exception(
                'invalid test for %s: %s' % (action, json.dumps(test, indent=2)))

        if "error" in response:
            with pytest.raises(RPCException):
                result = method(**args)
            return

        result = method(**args)
        request_made = client.session.adapter.last_request.json()

        assert request_made == request

        if result != expected:
            print('result:')
            print(json.dumps(result, indent=2, sort_keys=True))
            print('expected:')
            print(json.dumps(expected, indent=2, sort_keys=True))

        assert result == expected
