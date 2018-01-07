import requests

class Client(object):
    """ RaiBlocks node RPC client """

    def __init__(self, host=None, session=None):
        if not host:
            host = 'http://localhost:7076/'

        if not host.endswith('/'):
            host = host + '/'

        if not session:
            session = requests.Session()

        self.session = session
        self.host = host

    def call(self, action, params=None):
        params = params or {}

        params['action'] = action

        try:
            resp = self.session.post(self.host, json=params)
        except Exception:
            raise

        return resp.json()

    def version(self):
        """
        Returns the node's RPC version

        >>> rpc.version()
        {
            "rpc_version": 1,
            "store_version": 10,
            "node_vendor": "RaiBlocks 9.0"
        }

        """

        resp = self.call('version')

        for key in ('rpc_version', 'store_version'):
            resp[key] = int(resp[key])

        return resp
