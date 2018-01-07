import pytest
import requests
import requests_mock
from conftest import MockRPCMatchException


class TestMockRPCSession(object):
    def test_existing_request(self, mock_rpc_session):
        resp = mock_rpc_session.post(
            'mock://localhost:7076/', json={
                "action": "version"
            }
        )
        assert resp.json() == {
            u'rpc_version': u'1',
            u'node_vendor': u'RaiBlocks 7.5.0',
            u'store_version': u'2'
        }

    def test_missing_request(self, mock_rpc_session):
        with pytest.raises(MockRPCMatchException):
            resp = mock_rpc_session.post(
                'mock://localhost:7076/', json={
                    "action": "DOES NOT EXIST"
                }
            )
