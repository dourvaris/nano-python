import pytest
import requests
import requests_mock

from raiblocks.client import Client
from conftest import MockRPCMatchException, load_mock_rpc_fixtures


mock_rpc_fixtures = load_mock_rpc_fixtures()


@pytest.fixture
def client(mock_rpc_session):
    return Client(host='mock://localhost:7076', session=mock_rpc_session)


class TestClient(object):

    def test_call_valid_action(self, client):
        assert client.call('version') == {
            "rpc_version": "1",
            "store_version": "10",
            "node_vendor": "RaiBlocks 9.0"
        }

    def test_call_invalid_action(self, client):

        with pytest.raises(MockRPCMatchException):
            assert client.call('versions')

    @pytest.mark.parametrize('action,functest', [
        (
            action,
            call.get('func', {})
        )
        for action, calls in mock_rpc_fixtures.items()
        for call in calls
    ])
    def test_rpc_methods(self, client, action, functest):
        try:
            method = getattr(client, action)
        except AttributeError:
            pytest.xfail("`%s` not yet implemented" % action)

        if 'result' not in functest:
            pytest.skip("missing python result to compare")

        args = functest.get('args') or {}

        assert method(**args) == functest['result']
