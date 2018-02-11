import six
import json
import requests


def doc_metadata(categories):
    """ Decorator to add doc metadata for docs generation """

    def wrapper(f):
        f.__doc_meta__ = {
            'categories': categories
        }
        return f
    return wrapper


class RPCException(Exception):
    """ Base class for RPC errors """


class RPCClient(object):
    """
    RaiBlocks node RPC client

    :param host: RPC server host, defaults to `'http://localhost:7076'`
    :param session: optional :py:class:`requests.Session` session to use for this client

    >>> from raiblocks.rpc import RPCClient
    >>> rpc = RPCClient('http://localhost:7076')
    >>> rpc.version()
    {
        'rpc_version': 1,
        'store_version': 10,
        'node_vendor': 'RaiBlocks 9.0'
    }
    """

    def __init__(self, host='http://localhost:7076', session=None):
        """
        Initialize the RaiBlocks RPC client

        :param host: location of the RPC server eg. http://localhost:7076
        :type host: str

        :param session: optional `requests` session to use for this client
        :type host: :py:class:`requests.Session`

        """

        if not session:
            session = requests.Session()

        self.session = session
        self.host = host

    def call(self, action, params=None):
        """
        Makes an RPC call to the server and returns the json response

        :param action: RPC method to call
        :type action: str

        :param params: Dict of arguments to send with RPC call
        :type params: dict

        :raises: :py:exc:`raiblocks.rpc.RPCException`
        :raises: :py:exc:`requests.exceptions.RequestException`

        >>> rpc.call(
        ...     action='account_balance',
        ...     params={
        ...         'account': xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3'
        ...     })
        {'balance': '325586539664609129644855132177',
         'pending': '2309370940000000000000000000000000'}

        """
        params = params or {}
        params['action'] = action

        resp = self.session.post(self.host, json=params)
        result = resp.json()

        if 'error' in result:
            raise RPCException(result['error'])

        return result

    def _process_value(self, value, type):
        """
        Process a value that will be sent to backend

        :param value: the value to return

        :param type: hint for what sort of value this is
        :type type: str

        """

        if not isinstance(value, six.string_types + (list,)):
            value = json.dumps(value)
        return value

    @doc_metadata(categories=['account'])
    def account_balance(self, account):
        """
        Returns how many RAW is owned and how many have not yet been received
        by **account**

        :param account: Account id to return balance of
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_balance(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        {
          "balance": 10000,
          "pending": 10000
        }

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('account_balance', payload)

        for k, v in resp.items():
            resp[k] = int(v)

        return resp

    @doc_metadata(categories=['account'])
    def accounts_balances(self, accounts):
        """
        Returns how many RAW is owned and how many have not yet been received
        by **accounts** list

        :param accounts: list of accounts to return balances for
        :type accounts: list of str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.accounts_balances(
        ...     accounts=[
        ...         "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...         "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"
        ...      ]
        ... )
        {
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": {
                "balance": 10000,
                "pending": 10000
            },
            "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7": {
                "balance": 10000000,
                "pending": 0
            }
        }

        """

        accounts = self._process_value(accounts, 'list')

        payload = {
            "accounts": accounts,
        }

        resp = self.call('accounts_balances', payload)
        accounts_balances = resp.get('balances') or {}

        for account, balances in accounts_balances.items():
            for k in balances:
                balances[k] = int(balances[k])

        return accounts_balances

    @doc_metadata(categories=['account'])
    def account_block_count(self, account):
        """
        Get number of blocks for a specific **account**

        :param account: Account to get number of blocks for
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_block_count(account="xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3")
        19

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('account_block_count', payload)

        return int(resp['block_count'])

    @doc_metadata(categories=['wallet', 'account'])
    def accounts_create(self, wallet, count, work=True):
        """
        Creates new accounts, insert next deterministic keys in **wallet** up
        to **count**

        .. enable_control required
        .. version 8.0 required

        :param wallet: Wallet to create new accounts in
        :type wallet: str

        :param count: Number of accounts to create
        :type count: int

        :param work: If false, disables work generation after creating account
        :type work: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.accounts_create(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     count=2
        ... )
        [
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3s00000000"
        ]

        """

        wallet = self._process_value(wallet, 'wallet')
        count = self._process_value(count, 'int')

        payload = {
            "wallet": wallet,
            "count": count,
        }

        if not work:
            payload['work'] = self._process_value(work, 'strbool')

        resp = self.call('accounts_create', payload)

        return resp.get('accounts') or []

    @doc_metadata(categories=['account'])
    def accounts_frontiers(self, accounts):
        """
        Returns a list of pairs of account and block hash representing the
        head block for **accounts** list

        :param accounts: Accounts to return frontier blocks for
        :type accounts: list of str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.accounts_frontiers(
        ...     accounts=[
        ...         "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
        ...         "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"
        ...     ]
        ... )
        {
            "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3":
                "791AF413173EEE674A6FCF633B5DFC0F3C33F397F0DA08E987D9E0741D40D81A",
            "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7":
                "6A32397F4E95AF025DE29D9BF1ACE864D5404362258E06489FABDBA9DCCC046F"
        }

        """

        accounts = self._process_value(accounts, 'list')

        payload = {
            "accounts": accounts,
        }

        resp = self.call('accounts_frontiers', payload)

        return resp.get('frontiers') or {}

    @doc_metadata(categories=['account'])
    def account_info(self, account, representative=False, weight=False,
                     pending=False):
        """
        Returns frontier, open block, change representative block, balance,
        last modified timestamp from local database & block count for
        **account**

        :param account: Account to return info for
        :type account: str

        :param representative: if True, also returns the representative block
        :type representative: bool

        :param weight: if True, also returns the voting weight
        :type weight: bool

        :param pending: if True, also returns the pending balance
        :type pending: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_info(
        ...     account="xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
        ... )
        {
          "frontier": "FF84533A571D953A596EA401FD41743AC85D04F406E76FDE4408EAED50B473C5",
          "open_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
          "representative_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
          "balance": "235580100176034320859259343606608761791",
          "modified_timestamp": "1501793775",
          "block_count": "33"
        }

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        if representative:
            payload['representative'] = self._process_value(representative, 'strbool')
        if weight:
            payload['weight'] = self._process_value(weight, 'strbool')
        if pending:
            payload['pending'] = self._process_value(pending, 'strbool')

        resp = self.call('account_info', payload)

        for key in ('modified_timestamp', 'block_count', 'balance', 'pending', 'weight'):
            if key in resp:
                resp[key] = int(resp[key])

        return resp

    @doc_metadata(categories=['wallet', 'account'])
    def account_create(self, wallet, work=True):
        """
        Creates a new account, insert next deterministic key in **wallet**

        .. enable_control required

        :param wallet: Wallet to insert new account into
        :type wallet: str

        :param work: If false, disables work generation after creating account
        :type work: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_create(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        if not work:
            payload['work'] = self._process_value(work, 'strbool')

        resp = self.call('account_create', payload)

        return resp['account']

    @doc_metadata(categories=['account'])
    def account_get(self, key):
        """
        Get account number for the **public key**

        :param key: Public key to get account for
        :type key: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_get(
        ...    key="3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"
        ... )
        "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"

        """

        key = self._process_value(key, 'publickey')

        payload = {
            "key": key,
        }

        resp = self.call('account_get', payload)

        return resp['account']

    @doc_metadata(categories=['account'])
    def account_history(self, account, count):
        """
        Reports send/receive information for a **account**

        :param account: Account to get send/receive information for
        :type account: str

        :param count: number of blocks to return
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_history(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     count=1
        ... )
        [
            {
              "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
              "type": "receive",
              "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
              "amount": 100000000000000000000000000000000
            }
        ]

        """

        account = self._process_value(account, 'account')
        count = self._process_value(count, 'int')

        payload = {
            "account": account,
            "count": count,
        }

        resp = self.call('account_history', payload)
        history = resp.get('history') or []

        for entry in history:
            entry['amount'] = int(entry['amount'])

        return history

    @doc_metadata(categories=['wallet', 'account'])
    def account_list(self, wallet):
        """
        Lists all the accounts inside **wallet**

        :param wallet: Wallet to get account list for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_list(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        [
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ]

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('account_list', payload)

        return resp.get('accounts') or []

    @doc_metadata(categories=['wallet', 'account'])
    def account_move(self, source, wallet, accounts):
        """
        Moves **accounts** from **source** to **wallet**

        .. enable_control required

        :param source: wallet to move accounts from
        :type source: str

        :param wallet: wallet to move accounts to
        :type wallet: str

        :param accounts: accounts to move
        :type accounts: list of str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_move(
        ...     source="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     accounts=[
        ...         "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ...     ]
        ... )
        True

        """

        wallet = self._process_value(wallet, 'wallet')
        source = self._process_value(source, 'wallet')
        accounts = self._process_value(accounts, 'list')

        payload = {
            "wallet": wallet,
            "source": source,
            "accounts": accounts,
        }

        resp = self.call('account_move', payload)

        return resp['moved'] == '1'

    @doc_metadata(categories=['account'])
    def accounts_pending(self, accounts, count=None, threshold=None, source=False):
        """
        Returns a list of block hashes which have not yet been received by
        these **accounts**

        :param accounts: Accounts to return list of block hashes for
        :type accounts: list of str

        :param count: Max number of blocks to returns
        :type count: int

        :param threshold: Minimum amount in raw per block
        :type threshold: int

        :param source: if True returns the source as well
        :type source: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.accounts_pending(
        ...     accounts=[
        ...         "xrb_1111111111111111111111111111111111111111111111111117353trpda",
        ...         "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
        ...     ],
        ...     count=1
        ... )
        {
            "xrb_1111111111111111111111111111111111111111111111111117353trpda": [
                "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D"
            ],
            "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": [
                "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74"
            ]
        }

        """

        payload = {
            "accounts": accounts,
        }

        accounts = self._process_value(accounts, 'list')
        if count is not None:
            payload['count'] = self._process_value(count, 'int')

        if threshold is not None:
            payload['threshold'] = self._process_value(threshold, 'int')

        if source:
            payload['source'] = self._process_value(source, 'strbool')

        resp = self.call('accounts_pending', payload)

        blocks = resp.get('blocks') or {}
        for account, data in blocks.items():
            if isinstance(data, list):  # list of block hashes, no change needed
                continue
            if not data:
                blocks[account] = []  # convert a "" response to []
                continue
            for key, value in data.items():
                if isinstance(value, six.string_types):  # amount
                    data[key] = int(value)
                elif isinstance(value, dict):  # dict with "amount" and "source"
                    for key in ('amount',):
                        if key in value:
                            value[key] = int(value[key])

        return blocks

    @doc_metadata(categories=['account'])
    def account_key(self, account):
        """
        Get the public key for **account**

        :param account: Account to get public key for
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_key(
        ...     account="xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
        ... )
        "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('account_key', payload)

        return resp['key']

    @doc_metadata(categories=['account', 'wallet'])
    def account_remove(self, wallet, account):
        """
        Remove **account** from **wallet**

        .. enable_control required

        :param wallet: Wallet to remove account from
        :type wallet: str

        :param account: Account to remove
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_remove(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
        ... )
        True

        """

        wallet = self._process_value(wallet, 'wallet')
        account = self._process_value(account, 'account')

        payload = {
            "wallet": wallet,
            "account": account,
        }

        resp = self.call('account_remove', payload)

        return resp['removed'] == '1'

    @doc_metadata(categories=['account'])
    def account_representative(self, account):
        """
        Returns the representative for **account**

        :param account: Account to get representative for
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_representative(
        ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
        )
        "xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('account_representative', payload)

        return resp['representative']

    @doc_metadata(categories=['wallet', 'account'])
    def account_representative_set(self, wallet, account, representative, work=None):
        """
        Sets the representative for **account** in **wallet**

        .. enable_control required

        :param wallet: Wallet to use for account
        :type wallet: str

        :param account: Account to set representative for
        :type account: str

        :param representative: Representative to set to
        :type representative: str

        :param work: If set, is used as the work for the block
        :type work: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_representative_set(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi",
        ...     representative="xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"
        ... )
        "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"

        """

        wallet = self._process_value(wallet, 'wallet')
        account = self._process_value(account, 'account')
        representative = self._process_value(representative, 'account')

        payload = {
            "wallet": wallet,
            "account": account,
            "representative": representative,
        }

        if work is not None:
            payload['work'] = self._process_value(work, 'work')

        resp = self.call('account_representative_set', payload)

        return resp['block']

    @doc_metadata(categories=['account'])
    def account_weight(self, account):
        """
        Returns the voting weight for **account**

        :param account: Account to get voting weight for
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.account_weight(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        10000

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('account_weight', payload)

        return int(resp['weight'])

    @doc_metadata(categories=['global'])
    def available_supply(self):
        """
        Returns how many rai are in the public supply

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.available_supply()
        10000

        """

        resp = self.call('available_supply')

        return int(resp['available'])

    @doc_metadata(categories=['block'])
    def block(self, hash):
        """
        Retrieves a json representation of **block**

        :param hash: Hash of block to return representation for
        :type hash: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.block(
        ...     hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
            "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "work": "0000000000000000",
            "source": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
            "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "type": "open"
        }

        """

        hash = self._process_value(hash, 'block')

        payload = {
            "hash": hash,
        }

        resp = self.call('block', payload)

        return json.loads(resp['contents'])

    @doc_metadata(categories=['block'])
    def blocks(self, hashes):
        """
        Retrieves a json representations of **blocks**

        :param hashes: List of block hashes to return
        :type hashes: list of str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.blocks(
        ...     hashes=["000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"]
        ... )
        {
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F": {
                "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                "work": "0000000000000000",
                "source": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
                "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                "signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "type": "open"
            }
        }

        """

        hashes = self._process_value(hashes, 'list')

        payload = {
            "hashes": hashes,
        }

        resp = self.call('blocks', payload)
        blocks = resp.get('blocks') or {}

        for k, v in blocks.items():
            blocks[k] = json.loads(v)

        return blocks

    @doc_metadata(categories=['block'])
    def blocks_info(self, hashes, pending=False, source=False):
        """
        Retrieves a json representations of **blocks** with transaction
        **amount** & block **account**

        :param hashes: List of block hashes to return info for
        :type hashes: list of str

        :param pending: If true, returns pending amount as well
        :type pending: bool

        :param source: If true, returns source account as well
        :type source: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.blocks_info(hashes=["000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"])
        {
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F": {
                "block_account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                "amount": "1000000000000000000000000000000",
                "contents": {
                    "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                    "work": "0000000000000000",
                    "source": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
                    "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                    "signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                    "type": "open"
                }
            }
        }

        """

        hashes = self._process_value(hashes, 'list')

        payload = {
            "hashes": hashes,
        }

        if pending:
            payload['pending'] = self._process_value(pending, 'strbool')
        if source:
            payload['source'] = self._process_value(source, 'strbool')

        resp = self.call('blocks_info', payload)

        blocks = resp.get('blocks') or {}

        for block, data in blocks.items():
            data['contents'] = json.loads(data['contents'])
            for key in ('amount', 'pending'):
                if key in data:
                    data[key] = int(data[key])

        return blocks

    @doc_metadata(categories=['account', 'block'])
    def block_account(self, hash):
        """
        Returns the account containing block

        :param hash: Hash of the block to return account for
        :type hash: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.block_account(
        ...     hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        hash = self._process_value(hash, 'block')

        payload = {
            "hash": hash,
        }

        resp = self.call('block_account', payload)

        return resp['account']

    @doc_metadata(categories=['global', 'block'])
    def block_count(self):
        """
        Reports the number of blocks in the ledger and unchecked synchronizing
        blocks

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.block_count()
        {
          "count": 1000,
          "unchecked": 10
        }

        """

        resp = self.call('block_count')

        for k, v in resp.items():
            resp[k] = int(v)

        return resp

    @doc_metadata(categories=['global', 'block'])
    def block_count_type(self):
        """
        Reports the number of blocks in the ledger by type (send, receive,
        open, change)

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.block_count_type()
        {
          "send": 1000,
          "receive": 900,
          "open": 100,
          "change": 50
        }

        """

        resp = self.call('block_count_type')

        for k, v in resp.items():
            resp[k] = int(v)

        return resp

    @doc_metadata(categories=['block'])
    def block_create(self,
                     type,
                     account,
                     wallet=None,
                     representative=None,
                     key=None,
                     destination=None,
                     amount=None,
                     balance=None,
                     previous=None,
                     source=None,
                     work=None):
        """
        Creates a json representations of new block based on input data &
        signed with private key or account in **wallet** for offline signing

        .. enable_control required
        .. version 8.1 required

        :param type: Type of block to create one of **open**, **receive**,
                     **change**, **send**
        :type type: str

        :param account: Account for the signed block
        :type account: str

        :param wallet: Wallet to use
        :type wallet: str

        :param representative: Representative account for **open** and
                               **change** blocks
        :type representative: str

        :param key: Private key to use to open account for **open** blocks
        :type key: str

        :param destination: Destination account for **send** blocks
        :type destination: str

        :param amount: Amount in raw for **send** blocks
        :type amount: int

        :param balance: Balance in raw of account for **send** blocks
        :type balance: int

        :param previous: Previous block hash for **receive**, **send**
                       and **change** blocks
        :type previous: str

        :param source: Source block for **open** and **receive** blocks
        :type source: str

        :param work: Work value to use for block from external source
        :type work: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.block_create(
        ...     type="open",
        ...     account="xrb_3kdbxitaj7f6mrir6miiwtw4muhcc58e6tn5st6rfaxsdnb7gr4roudwn951",
        ...     source="19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
        ...     representative="xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",
        ...     key="0000000000000000000000000000000000000000000000000000000000000001"
        ... )
        {
            "block": {
                "account": "xrb_3kdbxitaj7f6mrir6miiwtw4muhcc58e6tn5st6rfaxsdnb7gr4roudwn951",
                "representative": "xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",
                "signature": "5974324F8CC42DA56F62FC212A17886BDCB18DE363D04DA84EEDC99CB4A33919D14A2CF9DE9D534FAA6D0B91D01F0622205D898293525E692586C84F2DCF9208",
                "source": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
                "type": "open",
                "work": "4ec76c9bda2325ed"
            },
            "hash": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4"
        }

        >>> rpc.block_create(
        ...     type="receive",
        ...     account="xrb_3kdbxitaj7f6mrir6miiwtw4muhcc58e6tn5st6rfaxsdnb7gr4roudwn951",
        ...     previous="F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4",
        ...     source="19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ... )
        {
            "block": {
                "previous": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4",
                "signature": "A13FD22527771667D5DFF33D69787D734836A3561D8A490C1F4917A05D77EA09860461D5FBFC99246A4EAB5627F119AD477598E22EE021C4711FACF4F3C80D0E",
                "source": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
                "type": "receive",
                "work": "6acb5dd43a38d76a"
            },
            "hash": "314BA8D9057678C1F53371C2DB3026C1FAC01EC8E7802FD9A2E8130FC523429E"
        }

        >>> rpc.block_create(
        ...     type="send",
        ...     account="xrb_3kdbxitaj7f6mrir6miiwtw4muhcc58e6tn5st6rfaxsdnb7gr4roudwn951",
        ...     amount=10000000000000000000000000000000,
        ...     balance=20000000000000000000000000000000,
        ...     destination="xrb_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",
        ...     previous="314BA8D9057678C1F53371C2DB3026C1FAC01EC8E7802FD9A2E8130FC523429E",
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     work="478563b2d9facfd4",
        ... )
        {
            "block": {
                "balance": "0000007E37BE2022C0914B2680000000",
                "destination": "xrb_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",
                "previous": "314BA8D9057678C1F53371C2DB3026C1FAC01EC8E7802FD9A2E8130FC523429E",
                "signature": "F19CA177EFA8692C8CBF7478CE3213F56E4A85DF760DA7A9E69141849831F8FD79BA9ED89CEC807B690FB4AA42D5008F9DBA7115E63C935401F1F0EFA547BC00",
                "type": "send",
                "work": "478563b2d9facfd4"
            },
            "hash": "F958305C0FF0551421D4ABEDCCF302079D020A0A3833E33F185E2B0415D4567A"
        }

        >>> rpc.block_create(
        ...     type="change",
        ...     account="xrb_3kdbxitaj7f6mrir6miiwtw4muhcc58e6tn5st6rfaxsdnb7gr4roudwn951",
        ...     representative="xrb_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",
        ...     previous="F958305C0FF0551421D4ABEDCCF302079D020A0A3833E33F185E2B0415D4567A",
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ... )
        {
            "block": {
                "previous": "F958305C0FF0551421D4ABEDCCF302079D020A0A3833E33F185E2B0415D4567A",
                "representative": "xrb_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",
                "signature": "98B4D56881D9A88B170A6B2976AE21900C26A27F0E2C338D93FDED56183B73D19AA5BEB48E43FCBB8FF8293FDD368CEF50600FECEFD490A0855ED702ED209E04",
                "type": "change",
                "work": "55e5b7a83edc3f4f"
            },
            "hash": "654FA425CEBFC9E7726089E4EDE7A105462D93DBC915FFB70B50909920A7D286"
        }
        """

        payload = {
            "type": self._process_value(type, 'blocktype'),
            "account": self._process_value(account, 'account'),
        }

        if representative is not None:
            payload['representative'] = self._process_value(representative, 'account')

        if key is not None:
            payload['key'] = self._process_value(key, 'privatekey')

        if source is not None:
            payload['source'] = self._process_value(source, 'block')

        if destination is not None:
            payload['destination'] = self._process_value(destination, 'account')

        if amount is not None:
            payload['amount'] = self._process_value(amount, 'int')

        if balance is not None:
            payload['balance'] = self._process_value(balance, 'int')

        if previous is not None:
            payload['previous'] = self._process_value(previous, 'block')

        if wallet is not None:
            payload['wallet'] = self._process_value(wallet, 'wallet')

        if work is not None:
            payload['work'] = self._process_value(work, 'work')

        resp = self.call('block_create', payload)
        resp['block'] = json.loads(resp['block'])

        return resp

    @doc_metadata(categories=['node'])
    def bootstrap(self, address, port):
        """
        Initialize bootstrap to specific **IP address** and **port**

        :param address: Ip address to bootstrap
        :type address: str

        :param port: Port to bootstrap
        :type port: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.bootstrap(address="::ffff:138.201.94.249", port="7075")
        True
        """

        address = self._process_value(address, 'ipaddr')
        port = self._process_value(port, 'int')

        payload = {
            "address": address,
            "port": port,
        }

        resp = self.call('bootstrap', payload)

        return 'success' in resp

    @doc_metadata(categories=['node'])
    def bootstrap_any(self):
        """
        Initialize multi-connection bootstrap to random peers

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.bootstrap_any()
        True
        """

        resp = self.call('bootstrap_any')

        return 'success' in resp

    @doc_metadata(categories=['block'])
    def chain(self, block, count):
        """
        Returns a list of block hashes in the account chain starting at
        **block** up to **count**

        :param block: Block hash to start at
        :type block: str

        :param count: Number of blocks to return up to
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.chain(
        ...     block="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     count=1
        ... )
        [
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ]

        """

        block = self._process_value(block, 'block')
        count = self._process_value(count, 'int')

        payload = {
            "block": block,
            "count": count,
        }

        resp = self.call('chain', payload)

        return resp.get('blocks') or []

    @doc_metadata(categories=['account'])
    def delegators(self, account):
        """
        Returns a list of pairs of delegator names given **account** a
        representative and its balance

        .. version 8.0 required

        :param account: Account to return delegators for
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.delegators(
        ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda"
        ... )
        {
            "xrb_13bqhi1cdqq8yb9szneoc38qk899d58i5rcrgdk5mkdm86hekpoez3zxw5sd":
                "500000000000000000000000000000000000",
            "xrb_17k6ug685154an8gri9whhe5kb5z1mf5w6y39gokc1657sh95fegm8ht1zpn":
                "961647970820730000000000000000000000"
        }

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('delegators', payload)
        delegators = resp.get('delegators') or {}

        for k, v in delegators.items():
            delegators[k] = int(v)

        return delegators

    @doc_metadata(categories=['account'])
    def delegators_count(self, account):
        """
        Get number of delegators for a specific representative **account**

        .. version 8.0 required

        :param account: Account to get number of delegators for
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.delegators_count(
        ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda"
        ... )
        2

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('delegators_count', payload)

        return int(resp['count'])

    @doc_metadata(categories=['utility'])
    def deterministic_key(self, seed, index):
        """
        Derive deterministic keypair from **seed** based on **index**

        :param seed: Seed used to get keypair
        :type seed: str

        :param index: Index of the generated keypair
        :type index: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.deterministic_key(
        ...     seed="0000000000000000000000000000000000000000000000000000000000000000",
        ...     index=0
        ... )
        {
          "private": "9F0E444C69F77A49BD0BE89DB92C38FE713E0963165CCA12FAF5712D7657120F",
          "public": "C008B814A7D269A1FA3C6528B19201A24D797912DB9996FF02A1FF356E45552B",
          "account": "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"
        }

        """

        seed = self._process_value(seed, 'seed')
        index = self._process_value(index, 'int')

        payload = {
            "seed": seed,
            "index": index,
        }

        resp = self.call('deterministic_key', payload)

        return resp

    @doc_metadata(categories=['account'])
    def frontiers(self, account, count):
        """
        Returns a list of pairs of account and block hash representing the
        head block starting at **account** up to **count**

        :param account: Account to get frontier blocks for
        :type account: str

        :param count: Max amount to return
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.frontiers(
        ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
        ...     count=1
        ... )
        {
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000":
                "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        }

        """

        account = self._process_value(account, 'account')
        count = self._process_value(count, 'int')

        payload = {
            "account": account,
            "count": count,
        }

        resp = self.call('frontiers', payload)

        return resp.get('frontiers') or {}

    @doc_metadata(categories=['global'])
    def frontier_count(self):
        """
        Reports the number of accounts in the ledger

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.frontier_count()
        1000

        """

        resp = self.call('frontier_count')

        return int(resp['count'])

    @doc_metadata(categories=['block'])
    def history(self, hash, count):
        """
        Reports send/receive information for a chain of blocks

        :param hash: Hash of block to receive history for
        :type hash: str

        :param count: Max number of blocks to return
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.history(
        ...     hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     count=1
        ... )
        [
            {
              "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
              "type": "receive",
              "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
              "amount": "100000000000000000000000000000000"
            }
        ]

        """

        hash = self._process_value(hash, 'block')
        count = self._process_value(count, 'int')

        payload = {
            "hash": hash,
            "count": count,
        }

        resp = self.call('history', payload)

        history = resp.get('history') or []

        for entry in history:
            entry['amount'] = int(entry['amount'])

        return history

    @doc_metadata(categories=['utility'])
    def mrai_from_raw(self, amount):
        """
        Divide a raw amount down by the Mrai ratio.

        :param amount: Amount in raw to convert to Mrai
        :type amount: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.mrai_from_raw(amount=1000000000000000000000000000000)
        1

        """

        amount = self._process_value(amount, 'int')

        payload = {
            "amount": amount,
        }

        resp = self.call('mrai_from_raw', payload)

        return int(resp['amount'])

    @doc_metadata(categories=['utility'])
    def mrai_to_raw(self, amount):
        """
        Multiply an Mrai amount by the Mrai ratio.

        :param amount: Amount in Mrai to convert to raw
        :type amount: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.mrai_to_raw(amount=1)
        1000000000000000000000000000000

        """

        amount = self._process_value(amount, 'int')

        payload = {
            "amount": amount,
        }

        resp = self.call('mrai_to_raw', payload)

        return int(resp['amount'])

    @doc_metadata(categories=['utility'])
    def krai_from_raw(self, amount):
        """
        Divide a raw amount down by the krai ratio.

        :param amount: Amount in raw to convert to krai
        :type amount: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.krai_from_raw(amount=1000000000000000000000000000)
        1
        """

        amount = self._process_value(amount, 'int')

        payload = {
            "amount": amount,
        }

        resp = self.call('krai_from_raw', payload)

        return int(resp['amount'])

    @doc_metadata(categories=['utility'])
    def krai_to_raw(self, amount):
        """
        Multiply an krai amount by the krai ratio.

        :param amount: Amount in krai to convert to raw
        :type amount: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.krai_to_raw(amount=1)
        1000000000000000000000000000

        """

        amount = self._process_value(amount, 'int')

        payload = {
            "amount": amount,
        }

        resp = self.call('krai_to_raw', payload)

        return int(resp['amount'])

    @doc_metadata(categories=['utility'])
    def rai_from_raw(self, amount):
        """
        Divide a raw amount down by the rai ratio.

        :param amount: Amount in raw to convert to rai
        :type amount: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.rai_from_raw(amount=1000000000000000000000000)
        1

        """

        amount = self._process_value(amount, 'int')

        payload = {
            "amount": amount,
        }

        resp = self.call('rai_from_raw', payload)

        return int(resp['amount'])

    @doc_metadata(categories=['utility'])
    def rai_to_raw(self, amount):
        """
        Multiply an rai amount by the rai ratio.

        :param amount: Amount in rai to convert to raw
        :type amount: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.rai_to_raw(amount=1)
        1000000000000000000000000

        """

        amount = self._process_value(amount, 'int')

        payload = {
            "amount": amount,
        }

        resp = self.call('rai_to_raw', payload)

        return int(resp['amount'])

    @doc_metadata(categories=['utility'])
    def key_create(self):
        """
        Generates an **adhoc random keypair**

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.key_create()
        {
          "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
          "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
          "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
        }

        """

        resp = self.call('key_create')

        return resp

    @doc_metadata(categories=['utility'])
    def key_expand(self, key):
        """
        Derive public key and account number from **private key**

        :param key: Private key to generate account and public key of
        :type key: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.key_expand(
            key="781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
        )
        {
          "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
          "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
          "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
        }

        """

        key = self._process_value(key, 'privatekey')

        payload = {
            "key": key,
        }

        resp = self.call('key_expand', payload)

        return resp

    @doc_metadata(categories=['node'])
    def keepalive(self, address, port):
        """
        Tells the node to send a keepalive packet to **address**:**port**

        .. enable_control required

        :param address: IP address of node to send keepalive packet to
        :type address: str

        :param port: Port of node to send keepalive packet to
        :type port: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.keepalive(address="::ffff:192.168.1.1", port=1024)
        True
        """

        address = self._process_value(address, 'ipaddr')
        port = self._process_value(port, 'int')

        payload = {
            "address": address,
            "port": port,
        }

        resp = self.call('keepalive', payload)

        return resp == {}

    @doc_metadata(categories=['account'])
    def ledger(self, account, count=None, representative=False, weight=False,
               pending=False, sorting=False):
        """
        Returns frontier, open block, change representative block, balance,
        last modified timestamp from local database & block count starting at
        **account** up to **count**

        .. enable_control required
        .. version 8.0 required

        :param account: Account to return blocks for
        :type account: str

        :param count: Max number of blocks to return
        :type count: int

        :param representative: If true, returns the representative as well
        :type representative: bool

        :param weight: If true, returns the voting weight as well
        :type weight: bool

        :param pending: If true, returns the pending amount as well
        :type pending: bool

        :param sorting: If true, sorts the response by balance
        :type sorting: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.ledger(
        ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
        ...     count=1
        ... )
        {
            "xrb_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {
                "frontier": "E71AF3E9DD86BBD8B4620EFA63E065B34D358CFC091ACB4E103B965F95783321",
                "open_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
                "representative_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
                "balance": 0,
                "modified_timestamp": 1511476234,
                "block_count": 2
            }
        }

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        if count is not None:
            payload['count'] = self._process_value(count, 'int')

        if sorting:
            payload['sorting'] = self._process_value(sorting, 'strbool')

        if representative:
            payload['representative'] = self._process_value(representative, 'strbool')

        if weight:
            payload['weight'] = self._process_value(weight, 'strbool')

        if pending:
            payload['pending'] = self._process_value(pending, 'strbool')

        resp = self.call('ledger', payload)
        accounts = resp.get('accounts') or {}

        int_keys = (
            'balance', 'modified_timestamp', 'block_count', 'weight', 'pending'
        )
        for account, frontier in accounts.items():
            for key in int_keys:
                if key in frontier:
                    frontier[key] = int(frontier[key])

        return accounts

    @doc_metadata(categories=['wallet'])
    def payment_begin(self, wallet):
        """
        Begin a new payment session. Searches wallet for an account that's
        marked as available and has a 0 balance. If one is found, the account
        number is returned and is marked as unavailable. If no account is
        found, a new account is created, placed in the wallet, and returned.

        :param wallet: Wallet to begin payment in
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.payment_begin(
        ... wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('payment_begin', payload)

        return resp['account']

    # NOTE(dan): Server RPC is broken here - it *should* return an
    # 'error' for 'No wallet found', but it returns 'status' instead
    # https://github.com/clemahieu/raiblocks/blob/e9592e5/rai/node/rpc.cpp#L2238
    @doc_metadata(categories=['wallet'])
    def payment_init(self, wallet):
        """
        Marks all accounts in wallet as available for being used as a payment
        session.

        :param wallet: Wallet to init payment in
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.payment_init(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('payment_init', payload)

        return resp['status'] == 'Ready'

    @doc_metadata(categories=['wallet'])
    def payment_end(self, account, wallet):
        """
        End a payment session.  Marks the account as available for use in a
        payment session.

        :param account: Account to mark available
        :type account: str

        :param wallet: Wallet to end payment session for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.payment_end(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     wallet="FFFD1BAEC8EC20814BBB9059B393051AAA8380F9B5A2E6B2489A277D81789EEE"
        ... )
        True
        """

        account = self._process_value(account, 'account')
        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "account": account,
            "wallet": wallet,
        }

        resp = self.call('payment_end', payload)

        return resp == {}

    @doc_metadata(categories=['account'])
    def payment_wait(self, account, amount, timeout):
        """
        Wait for payment of **amount** to arrive in **account** or until **timeout**
        milliseconds have elapsed.

        :param account: Account to wait for payment
        :type account: str

        :param amount: Amount in raw of funds to wait for payment to arrive
        :type amount: int

        :param timeout: Timeout in milliseconds to wait for
        :type timeout: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.payment_wait(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     amount=1,
        ...     timeout=1000
        ... )
        True

        """

        account = self._process_value(account, 'account')
        amount = self._process_value(amount, 'int')
        timeout = self._process_value(timeout, 'int')

        payload = {
            "account": account,
            "amount": amount,
            "timeout": timeout,
        }

        resp = self.call('payment_wait', payload)

        return resp['status'] == 'success'

    @doc_metadata(categories=['block'])
    def process(self, block):
        """
        Publish **block** to the network

        :param block: Block to publish
        :type block: dict or json

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> block = {
            "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "work": "0000000000000000",
            "source": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
            "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "type": "open"
        }

        >>> rpc.process(block=block)
        "42A723D2B60462BF7C9A003FE9A70057D3A6355CA5F1D0A57581000000000000"

        >>> rpc.process(json.dumps(block))
        "42A723D2B60462BF7C9A003FE9A70057D3A6355CA5F1D0A57581000000000000"

        """

        if isinstance(block, dict):
            block = json.dumps(block, sort_keys=True)

        payload = {
            "block": block,
        }

        resp = self.call('process', payload)

        return resp['hash']

    @doc_metadata(categories=['wallet', 'account', 'block'])
    def receive(self, wallet, account, block, work=None):
        """
        Receive pending **block** for **account** in **wallet**

        .. enable_control required

        :param wallet: Wallet of account to receive block for
        :type wallet: str

        :param account: Account to receive block for
        :type account: str

        :param block: Block hash to receive
        :type block: str

        :param work: If set, uses this work for the receive block
        :type work: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.receive(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     block="53EAA25CE28FA0E6D55EA9704B32604A736966255948594D55CBB05267CECD48",
        ...     work="12041e830ad10de1"
        ... )
        "EE5286AB32F580AB65FD84A69E107C69FBEB571DEC4D99297E19E3FA5529547B"

        """

        wallet = self._process_value(wallet, 'wallet')
        account = self._process_value(account, 'account')
        block = self._process_value(block, 'block')

        payload = {
            "wallet": wallet,
            "account": account,
            "block": block,
        }

        if work:
            payload['work'] = self._process_value(work, 'work')

        resp = self.call('receive', payload)

        return resp['block']

    @doc_metadata(categories=['node'])
    def receive_minimum(self):
        """
        Returns receive minimum for node

        .. enable_control required
        .. version 8.0 required

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.receive_minimum()
        1000000000000000000000000

        """

        resp = self.call('receive_minimum')

        return int(resp['amount'])

    @doc_metadata(categories=['node'])
    def receive_minimum_set(self, amount):
        """
        Set **amount** as new receive minimum for node until restart

        .. enable_control required
        .. version 8.0 required

        :param amount: Amount in raw to set as minimum to receive
        :type amount: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.receive_minimum_set(amount=1000000000000000000000000000000)
        True
        """

        amount = self._process_value(amount, 'int')

        payload = {
            "amount": amount,
        }

        resp = self.call('receive_minimum_set', payload)

        return 'success' in resp

    @doc_metadata(categories=['global'])
    def representatives(self, count=None, sorting=False):
        """
        Returns a list of pairs of representative and its voting weight

        :param count: Max amount of representatives to return
        :type count: int

        :param sorting: If true, sorts by weight
        :type sorting: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.representatives()
        {
            "xrb_1111111111111111111111111111111111111111111111111117353trpda":
                3822372327060170000000000000000000000,
            "xrb_1111111111111111111111111111111111111111111111111awsq94gtecn":
                30999999999999999999999999000000,
            "xrb_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi":
                0
        }


        """
        payload = {}

        if count is not None:
            payload['count'] = self._process_value(count, 'int')

        if sorting:
            payload['sorting'] = self._process_value(sorting, 'strbool')

        resp = self.call('representatives', payload)

        representatives = resp.get('representatives') or {}

        for k, v in representatives.items():
            representatives[k] = int(v)

        return representatives

    @doc_metadata(categories=['node', 'block'])
    def unchecked(self, count=None):
        """
        Returns a list of pairs of unchecked synchronizing block hash and its
        json representation up to **count**

        .. version 8.0 required

        :param count: Max amount of unchecked blocks to return
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.unchecked(count=1)
        {
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F": {
                "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                "work": "0000000000000000",
                "source": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
                "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                "signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                "type": "open"
            }
        }

        """

        payload = {}

        if count is not None:
            payload["count"] = self._process_value(count, 'int')

        resp = self.call('unchecked', payload)

        blocks = resp.get('blocks') or {}
        for block, block_json in blocks.items():
            blocks[block] = json.loads(block_json)

        return blocks

    @doc_metadata(categories=['node', 'block'])
    def unchecked_clear(self):
        """
        Clear unchecked synchronizing blocks

        .. enable_control required
        .. version 8.0 required

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.unchecked_clear()
        True

        """

        resp = self.call('unchecked_clear')

        return 'success' in resp

    @doc_metadata(categories=['node', 'block'])
    def unchecked_get(self, hash):
        """
        Retrieves a json representation of unchecked synchronizing block by
        **hash**

        .. version 8.0 required

        :param hash: Hash of unchecked block to get
        :type hash: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.unchecked_get(
        ...     hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
            "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "work": "0000000000000000",
            "source": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
            "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "type": "open"
        }

        """

        hash = self._process_value(hash, 'block')

        payload = {
            "hash": hash,
        }

        resp = self.call('unchecked_get', payload)

        return json.loads(resp['contents'])

    @doc_metadata(categories=['node', 'block'])
    def unchecked_keys(self, key=None, count=None):
        """
        Retrieves unchecked database keys, blocks hashes & a json
        representations of unchecked pending blocks starting from **key** up
        to **count**

        .. version 8.0 required

        :param key: Starting key to return unchecked keys for
        :type key: str

        :param count: Max number of keys/blocks to return
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.unchecked_keys(
        ...     key="FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
        ...     count=1
        ... )
        [
            {
                "key": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
                "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
                "contents": {
                    "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                    "work": "0000000000000000",
                    "source": "FA5B51D063BADDF345EFD7EF0D3C5FB115C85B1EF4CDE89D8B7DF3EAF60A04A4",
                    "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
                    "signature": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                    "type": "open"
                }
            }
        ]

        """

        payload = {}

        if key:
            payload['key'] = self._process_value(key, 'publickey')

        if count is not None:
            payload['count'] = self._process_value(count, 'int')

        resp = self.call('unchecked_keys', payload)
        unchecked = resp.get('unchecked') or []

        for entry in unchecked:
            entry['contents'] = json.loads(entry['contents'])

        return unchecked

    @doc_metadata(categories=['account'])
    def validate_account_number(self, account):
        """
        Check whether **account** is a valid account number

        :param account: Account number to check
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.validate_account_number(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        True
        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        resp = self.call('validate_account_number', payload)

        return resp['valid'] == '1'

    @doc_metadata(categories=['wallet'])
    def wallet_representative(self, wallet):
        """
        Returns the default representative for **wallet**

        :param wallet: Wallet to get default representative account for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_representative(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_representative', payload)

        return resp['representative']

    @doc_metadata(categories=['wallet'])
    def wallet_representative_set(self, wallet, representative):
        """
        Sets the default **representative** for **wallet**

        .. enable_control required

        :param wallet: Wallet to set default representative account for
        :type wallet: str

        :param representative: Representative account to set for **wallet**
        :type representative: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_representative_set(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     representative="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        True

        """

        wallet = self._process_value(wallet, 'wallet')
        representative = self._process_value(representative, 'account')

        payload = {
            "wallet": wallet,
            "representative": representative,
        }

        resp = self.call('wallet_representative_set', payload)

        return resp['set'] == '1'

    @doc_metadata(categories=['wallet'])
    def wallet_add(self, wallet, key, work=True):
        """
        Add an adhoc private key **key** to **wallet**

        .. enable_control required

        :param wallet: Wallet to add private key to
        :type wallet: str

        :param key: Private key to add
        :type key: str

        :param work: If false, disables work generation
        :type work: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_add(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     key="34F0A37AAD20F4A260F0A5B3CB3D7FB50673212263E58A380BC10474BB039CE4"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = self._process_value(wallet, 'wallet')
        key = self._process_value(key, 'privatekey')

        payload = {
            "wallet": wallet,
            "key": key,
        }

        if not work:
            payload['work'] = self._process_value(work, 'strbool')

        resp = self.call('wallet_add', payload)

        return resp['account']

    @doc_metadata(categories=['wallet'])
    def wallet_balance_total(self, wallet):
        """
        Returns the sum of all accounts balances in **wallet**

        :param wallet: Wallet to return sum of balances for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_balance_total(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
          "balance": 10000,
          "pending": 10000
        }

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_balance_total', payload)

        for k, v in resp.items():
            resp[k] = int(v)

        return resp

    @doc_metadata(categories=['wallet'])
    def wallet_balances(self, wallet):
        """
        Returns how many rai is owned and how many have not yet been received
        by all accounts in **wallet**

        :param wallet: Wallet to return balances for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_balances(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": {
                "balance": 10000,
                "pending": 10000
            }
        }

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_balances', payload)
        balances = resp.get('balances') or {}
        for account, balance in balances.items():
            for k, v in balances[account].items():
                balances[account][k] = int(v)

        return balances

    @doc_metadata(categories=['wallet'])
    def wallet_change_seed(self, wallet, seed):
        """
        Changes seed for **wallet** to **seed**

        .. enable_control required

        :param wallet: Wallet to change seed for
        :type wallet: str

        :param seed: Seed to change wallet to
        :type seed: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_change_seed(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     seed="74F2B37AAD20F4A260F0A5B3CB3D7FB51673212263E58A380BC10474BB039CEE"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')
        seed = self._process_value(seed, 'seed')

        payload = {
            "wallet": wallet,
            "seed": seed,
        }

        resp = self.call('wallet_change_seed', payload)

        return 'success' in resp

    @doc_metadata(categories=['wallet'])
    def wallet_contains(self, wallet, account):
        """
        Check whether **wallet** contains **account**

        :param wallet: Wallet to check contains **account**
        :type wallet: str

        :param account: Account to check exists in **wallet**
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_contains(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')
        account = self._process_value(account, 'account')

        payload = {
            "wallet": wallet,
            "account": account,
        }

        resp = self.call('wallet_contains', payload)

        return resp['exists'] == '1'

    @doc_metadata(categories=['wallet'])
    def wallet_create(self):
        """
        Creates a new random wallet id

        .. enable_control required

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_create()
        "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"

        """

        resp = self.call('wallet_create')

        return resp['wallet']

    @doc_metadata(categories=['wallet'])
    def wallet_destroy(self, wallet):
        """
        Destroys **wallet** and all contained accounts

        .. enable_control required

        :param wallet: Wallet to destroy
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_destroy(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_destroy', payload)

        return resp == {}

    @doc_metadata(categories=['wallet'])
    def wallet_export(self, wallet):
        """
        Return a json representation of **wallet**

        :param wallet: Wallet to export
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_export(wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F")
        {
            "0000000000000000000000000000000000000000000000000000000000000000": "0000000000000000000000000000000000000000000000000000000000000001"
        }
        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_export', payload)

        return json.loads(resp['json'])

    @doc_metadata(categories=['wallet'])
    def wallet_frontiers(self, wallet):
        """
        Returns a list of pairs of account and block hash representing the
        head block starting for accounts from **wallet**

        :param wallet: Wallet to return frontiers for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_frontiers(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        }

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_frontiers', payload)

        return resp.get('frontiers') or {}

    @doc_metadata(categories=['wallet'])
    def wallet_key_valid(self, wallet):
        """
        Returns if a **wallet** key is valid

        :param wallet: Wallet to check key is valid
        :type wallet: str

        >>> rpc.wallet_key_valid(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_key_valid', payload)

        return resp['valid'] == '1'

    @doc_metadata(categories=['wallet'])
    def wallet_lock(self, wallet):
        """
        Locks a **wallet**

        :param wallet: Wallet to lock
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_lock(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_lock', payload)

        return resp['locked'] == '1'

    @doc_metadata(categories=['wallet'])
    def wallet_locked(self, wallet):
        """
        Checks whether **wallet** is locked

        :param wallet: Wallet to check if locked
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_locked(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        False
        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_locked', payload)

        return resp['locked'] == '1'

    @doc_metadata(categories=['wallet'])
    def wallet_unlock(self, wallet, password):
        """
        Unlocks **wallet** using **password**

        :param wallet: Wallet to unlock
        :type wallet: str

        :param password: Password to enter
        :type password: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_unlock(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     password="test"
        ... )
        True

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
            "password": password,
        }

        resp = self.call('wallet_unlock', payload)

        return resp['valid'] == '1'

    @doc_metadata(categories=['wallet'])
    def wallet_pending(self, wallet, count=None, threshold=None, source=False):
        """
        Returns a list of block hashes which have not yet been received by
        accounts in this **wallet**

        .. enable_control required
        .. version 8.0 required

        :param wallet: Wallet to get list of pending block hashes for
        :type wallet: str

        :param count: Max amount of blocks to return
        :type count: int

        :param threshold: Minimum amount in raw per block
        :type threshold: int

        :param source: If true, returns source account as well
        :type source: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_pending(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     count=1
        ... )
        {
            "xrb_1111111111111111111111111111111111111111111111111117353trpda": [
                "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D"
            ],
            "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": [
                "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74"
            ]
        }

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        if count is not None:
            payload['count'] = self._process_value(count, 'int')

        if threshold is not None:
            payload['threshold'] = self._process_value(threshold, 'int')

        if source:
            payload['source'] = self._process_value(source, 'strbool')

        resp = self.call('wallet_pending', payload)

        blocks = resp.get('blocks') or {}
        for account, data in blocks.items():
            if isinstance(data, list):  # list of block hashes, no change needed
                continue
            if not data:
                blocks[account] = []  # convert a "" response to []
                continue
            for key, value in data.items():
                if isinstance(value, six.string_types):  # amount
                    data[key] = int(value)
                elif isinstance(value, dict):  # dict with "amount" and "source"
                    for key in ('amount',):
                        if key in value:
                            value[key] = int(value[key])

        return blocks or {}

    @doc_metadata(categories=['wallet'])
    def wallet_republish(self, wallet, count):
        """
        Rebroadcast blocks for accounts from **wallet** starting at frontier
        down to **count** to the network

        .. enable_control required
        .. version 8.0 required

        :param wallet: Wallet to rebroadcast blocks for
        :type wallet: str

        :param count: Max amount of blocks to rebroadcast since frontier block
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_republish(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     count=2
        ... )
        [
            "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
            "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293",
            "90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35"
        ]

        """

        wallet = self._process_value(wallet, 'wallet')
        count = self._process_value(count, 'int')

        payload = {
            "wallet": wallet,
            "count": count,
        }

        resp = self.call('wallet_republish', payload)

        return resp.get('blocks') or []

    @doc_metadata(categories=['work'])
    def wallet_work_get(self, wallet):
        """
        Returns a list of pairs of account and work from **wallet**

        .. enable_control required
        .. version 8.0 required

        :param wallet: Wallet to return work for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.wallet_work_get(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
            "xrb_1111111111111111111111111111111111111111111111111111hifc8npp":
                "432e5cf728c90f4f"
        }

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_work_get', payload)

        return resp.get('works') or {}

    @doc_metadata(categories=['wallet'])
    def password_change(self, wallet, password):
        """
        Changes the password for **wallet** to **password**

        .. enable_control required

        :param wallet: Wallet to change password for
        :type wallet: str

        :param password: Password to set
        :type password: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.password_change(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     password="test"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
            "password": password,
        }

        resp = self.call('password_change', payload)

        return resp['changed'] == '1'

    @doc_metadata(categories=['wallet'])
    def password_enter(self, wallet, password):
        """
        Enters the **password** in to **wallet**

        :param wallet: Wallet to enter password for
        :type wallet: str

        :param password: Password to enter
        :type password: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.password_enter(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     password="test"
        ... )
        True

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
            "password": password,
        }

        resp = self.call('password_enter', payload)

        return resp['valid'] == '1'

    @doc_metadata(categories=['wallet'])
    def password_valid(self, wallet):
        """
        Checks whether the password entered for **wallet** is valid

        :param wallet: Wallet to check password for
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.password_valid(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('password_valid', payload)

        return resp['valid'] == '1'

    @doc_metadata(categories=['node'])
    def peers(self):
        """
        Returns a list of pairs of peer IPv6:port and its node network version

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.peers()
        {
            "[::ffff:172.17.0.1]:32841": 3
        }
        """

        resp = self.call('peers')

        result = {}
        peers = resp.get('peers') or {}

        for host, version in peers.items():
            result[host] = int(version)

        return result

    @doc_metadata(categories=['account'])
    def pending(self, account, count=None, threshold=None, source=False):
        """
        Returns a list of pending block hashes with amount more or equal to
        **threshold**

        .. version 8.0 required

        :param account: Account to get list of pending block hashes for
        :type account: str

        :param count: Max blocks to return
        :type count: int

        :param threshold: Minimum amount in raw for blocks
        :type threshold: int

        :param source: If true, returns source address as well
        :type source: bool

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.pending(
        ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda"
        ... )
        [
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ]

        >>> rpc.pending(
        ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda",
        ...     count=1,
        ...     threshold=1000000000000000000000000
        ... )
        {
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F": "6000000000000000000000000000000"
        }

        """

        account = self._process_value(account, 'account')

        payload = {
            "account": account,
        }

        if count is not None:
            payload['count'] = self._process_value(count, 'int')

        if threshold is not None:
            payload['threshold'] = self._process_value(threshold, 'int')

        if source:
            payload['source'] = self._process_value(source, 'strbool')

        resp = self.call('pending', payload)

        blocks = resp.get('blocks') or {}

        if isinstance(blocks, list):
            return blocks

        for block, value in blocks.items():
            if isinstance(value, six.string_types):  # amount
                blocks[block] = int(value)
            elif isinstance(value, dict):  # dict with "amount" and "source"
                for key in ('amount',):
                    if key in value:
                        value[key] = int(value[key])

        return blocks

    @doc_metadata(categories=['block'])
    def pending_exists(self, hash):
        """
        Check whether block is pending by **hash**

        .. version 8.0 required

        :param hash: Hash of block to check if pending
        :type hash: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.pending_exists(
            hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        )
        True
        """

        hash = self._process_value(hash, 'block')

        payload = {
            "hash": hash,
        }

        resp = self.call('pending_exists', payload)

        return resp['exists'] == '1'

    @doc_metadata(categories=['work'])
    def work_cancel(self, hash):
        """
        Stop generating **work** for block

        .. enable_control required

        :param hash: Hash to stop generating work for
        :type hash: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_cancel(
        ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
        ... )
        True

        """

        hash = self._process_value(hash, 'block')

        payload = {
            "hash": hash,
        }

        resp = self.call('work_cancel', payload)
        return resp == {}

    @doc_metadata(categories=['work'])
    def work_generate(self, hash):
        """
        Generates **work** for block

        .. enable_control required

        :param hash: Hash to start generating **work** for
        :type hash: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_generate(
        ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
        ... )
        "2bf29ef00786a6bc"

        """

        hash = self._process_value(hash, 'block')

        payload = {
            "hash": hash,
        }

        resp = self.call('work_generate', payload)

        return resp['work']

    @doc_metadata(categories=['work'])
    def work_get(self, wallet, account):
        """
        Retrieves work for **account** in **wallet**

        .. enable_control required
        .. version 8.0 required

        :param wallet: Wallet to get account work for
        :type wallet: str

        :param account: Account to get work for
        :type account: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_get(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp"
        ... )
        "432e5cf728c90f4f"

        """

        wallet = self._process_value(wallet, 'wallet')
        account = self._process_value(account, 'account')

        payload = {
            "wallet": wallet,
            "account": account,
        }

        resp = self.call('work_get', payload)

        return resp['work']

    @doc_metadata(categories=['work'])
    def work_set(self, wallet, account, work):
        """
        Set **work** for **account** in **wallet**

        .. enable_control required
        .. version 8.0 required

        :param wallet: Wallet to set work for account for
        :type wallet: str

        :param account: Account to set work for
        :type account: str

        :param work: Work to set for account in wallet
        :type work: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_set(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
        ...     work="0000000000000000"
        ... )
        True
        """

        wallet = self._process_value(wallet, 'wallet')
        account = self._process_value(account, 'account')
        work = self._process_value(work, 'work')

        payload = {
            "wallet": wallet,
            "account": account,
            "work": work,
        }

        resp = self.call('work_set', payload)

        return 'success' in resp

    @doc_metadata(categories=['work'])
    def work_peer_add(self, address, port):
        """
        Add specific **IP address** and **port** as work peer for node until
        restart

        .. enable_control required
        .. version 8.0 required

        :param address: IP address of work peer to add
        :type address: str

        :param port: Port work peer to add
        :type port: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_peer_add(address="::ffff:172.17.0.1", port="7076")
        True

        """

        address = self._process_value(address, 'ipaddr')
        port = self._process_value(port, 'int')

        payload = {
            "address": address,
            "port": port,
        }

        resp = self.call('work_peer_add', payload)

        return 'success' in resp

    @doc_metadata(categories=['work'])
    def work_peers(self):
        """
        Retrieve work peers

        .. enable_control required
        .. version 8.0 required

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_peers()
        [
            "::ffff:172.17.0.1:7076"
        ]

        """

        resp = self.call('work_peers')

        return resp.get('work_peers') or []

    @doc_metadata(categories=['work'])
    def work_peers_clear(self):
        """
        Clear work peers node list until restart

        .. enable_control required
        .. version 8.0 required

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_peers_clear()
        True

        """

        resp = self.call('work_peers_clear')
        return 'success' in resp

    @doc_metadata(categories=['work', 'block'])
    def work_validate(self, work, hash):
        """
        Check whether **work** is valid for block

        :param work: Work to validate
        :type work: str

        :param hash: Hash of block to validate work for
        :type hash: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.work_validate(
        ...     work="2bf29ef00786a6bc",
        ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
        ... )
        True

        """

        work = self._process_value(work, 'work')
        hash = self._process_value(hash, 'block')

        payload = {
            "work": work,
            "hash": hash,
        }

        resp = self.call('work_validate', payload)

        return resp['valid'] == '1'

    @doc_metadata(categories=['block'])
    def republish(self, hash, count=None, sources=None, destinations=None):
        """
        Rebroadcast blocks starting at **hash** to the network

        :param hash: Hash of block to start rebroadcasting from
        :type hash: str

        :param count: Max number of blocks to rebroadcast
        :type count: int

        :param sources: If set, additionally rebroadcasts source chain blocks
                        for receive/open up to **sources** depth
        :type sources: int

        :param destinations: If set, additionally rebroadcasts destination chain
                             blocks for receive/open up to **destinations** depth
        :type destinations: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.republish(
        ...     hash="991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"
        ... )
        [
            "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
            "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
        ]

        """

        hash = self._process_value(hash, 'block')

        payload = {
            "hash": hash,
        }

        if count is not None:
            payload['count'] = self._process_value(count, 'int')

        if sources is not None:
            payload['sources'] = self._process_value(sources, 'int')

        if destinations is not None:
            payload['destinations'] = self._process_value(destinations, 'int')

        resp = self.call('republish', payload)

        return resp.get('blocks') or []

    @doc_metadata(categories=['wallet'])
    def search_pending(self, wallet):
        """
        Tells the node to look for pending blocks for any account in
        **wallet**

        .. enable_control required

        :param wallet: Wallet to search for pending blocks
        :type wallet: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.search_pending(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True

        """

        wallet = self._process_value(wallet, 'wallet')

        payload = {
            "wallet": wallet,
        }

        resp = self.call('search_pending', payload)

        return resp['started'] == '1'

    @doc_metadata(categories=['node'])
    def search_pending_all(self):
        """
        Tells the node to look for pending blocks for any account in all
        available wallets

        .. enable_control required
        .. version 8.0 required

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.search_pending_all()
        True

        """

        resp = self.call('search_pending_all')

        return 'success' in resp

    @doc_metadata(categories=['wallet', 'account'])
    def send(self, wallet, source, destination, amount, work=None):
        """
        Send **amount** from **source** in **wallet** to **destination**

        .. enable_control required

        :param wallet: Wallet of account used to send funds
        :type wallet: str

        :param source: Account to send funds from
        :type source: str

        :param destination: Account to send funds to
        :type destination: str

        :param amount: Amount in raw to send
        :type amount: int

        :param work: If set, uses this work for the block
        :type work: str

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.send(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     source="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     destination="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     amount=1000000,
        ...     work="2bf29ef00786a6bc"
        ... )
        "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"

        """

        wallet = self._process_value(wallet, 'wallet')
        source = self._process_value(source, 'account')
        destination = self._process_value(destination, 'account')
        amount = self._process_value(amount, 'int')

        payload = {
            "wallet": wallet,
            "source": source,
            "destination": destination,
            "amount": amount,
        }

        if work is not None:
            payload['work'] = self._process_value(work, 'work')

        resp = self.call('send', payload)

        return resp['block']

    @doc_metadata(categories=['block'])
    def successors(self, block, count):
        """
        Returns a list of block hashes in the account chain ending at
        **block** up to **count**

        :param block: Hash of block to start returning successors for
        :type block: str

        :param count: Max number of successor blocks to return
        :type count: int

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.successors(
        ...     block="991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
        ...     count=1
        ... )
        [
            "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
        ]

        """

        block = self._process_value(block, 'block')
        count = self._process_value(count, 'int')

        payload = {
            "block": block,
            "count": count,
        }

        resp = self.call('successors', payload)

        return resp.get('blocks') or []

    @doc_metadata(categories=['node'])
    def stop(self):
        """
        Stop the node

        .. enable_control required

        :raises: :py:exc:`raiblocks.rpc.RPCException`

        >>> rpc.stop()
        True

        """

        resp = self.call('stop')

        return 'success' in resp

    @doc_metadata(categories=['node'])
    def version(self):
        """
        Returns the node's RPC version

        :raises: :py:exc:`raiblocks.rpc.RPCException`

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
