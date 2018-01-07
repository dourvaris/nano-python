import requests
from raiblocks.models import Account


def preprocess_account(account_string):
    return Account(account_string)


class Client(object):
    """ RaiBlocks node RPC client """

    def __init__(self, host=None, session=None):
        """
        Initialize the RaiBlocks RPC client

        :param host: location of the RPC server eg. http://localhost:7076
        :param session: optional `requests` session to use for this client
        """
        if not host:
            host = 'http://localhost:7076'

        if not session:
            session = requests.Session()

        self._session = session
        self.host = host

    def call(self, action, params=None):
        params = params or {}

        params['action'] = action

        try:
            resp = self._session.post(self.host, json=params)
        except Exception:
            raise

        return resp.json()

    def account_balance(self, account):
        """
        Returns how many RAW is owned and how many have not yet been received
        by **account**

        :type account: str

        >>> rpc.account_balance(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        {
          "balance": 10000,
          "pending": 10000
        }

        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('account_balance', payload)

        return {
            k: int(v) for k, v in resp.items()
        }

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

    def stop(self):
        """
        Stop the node

        .. enable_control required

        >>> rpc.stop()
        True

        """

        resp = self.call('stop')

        return 'success' in resp
