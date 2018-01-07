import os
import json
import pytest
import requests
import requests_mock


class MockRPCMatchException(Exception):
    """ Exception used to check if a mock response is missing """


def load_mock_rpc_tests():
    mocks_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'rpc.json'
    )
    return json.loads(open(mocks_path, 'rb').read())


@pytest.fixture
def mock_rpc_session():
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.mount('mock', adapter)

    responses = {}

    def _text_callback(request, context):
        request_json = json.dumps(request.json(), sort_keys=True)
        if request_json not in responses:
            raise MockRPCMatchException(
                'Could not match mock request: %s' % json.dumps(
                    request.json(), sort_keys=True, indent=2))
        return responses[request_json]

    for action, tests in load_mock_rpc_tests().items():
        for test in tests:
            req_body = json.dumps(test['request'], sort_keys=True)
            res_body = json.dumps(test['response'], sort_keys=True)
            responses[req_body] = res_body

    adapter.register_uri(
        'POST',
        'mock://localhost:7076/',
        text=_text_callback,
    )

    return session
