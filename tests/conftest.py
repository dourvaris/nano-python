import json
import os
from collections import OrderedDict

import pytest
import requests
import requests_mock


class MockRPCMatchException(Exception):
    """ Exception used to check if a mock response is missing """


def load_mock_rpc_tests():
    jsons_directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'rpc'
    )

    result = OrderedDict()
    for filename in os.listdir(jsons_directory):
        if filename.endswith('.json'):
            action = filename[: -len('.json')]
            try:
                tests = json.load(open(os.path.join(jsons_directory, filename)))
            except Exception:
                print('Failed to load %s test' % filename)
                raise
            result[action] = tests
    return result


@pytest.fixture
def mock_rpc_session():
    adapter = requests_mock.Adapter()
    session = requests.Session()
    session.mount('mock', adapter)
    session.adapter = adapter

    responses = {}

    def _text_callback(request, context):
        request_json = json.dumps(request.json(), sort_keys=True)
        if request_json not in responses:
            raise MockRPCMatchException(
                'No mock response found for this request: %s'
                % json.dumps(request.json(), sort_keys=True, indent=2)
            )
        return responses[request_json]

    for action, tests in load_mock_rpc_tests().items():
        for test in tests:
            req_body = json.dumps(test['request'], sort_keys=True)
            res_body = json.dumps(test['response'], sort_keys=True)
            responses[req_body] = res_body

    adapter.register_uri('POST', 'mock://localhost:7076/', text=_text_callback)

    return session
