import six
import json
import requests
from raiblocks.models import Account, Wallet, PublicKey, Block


def preprocess_account(account_string):
    return Account(account_string)


def preprocess_wallet(wallet_string):
    return Wallet(wallet_string)


def preprocess_block(block_string):
    return Block(block_string)


def preprocess_public_key(public_key_string):
    return PublicKey(public_key_string)


def preprocess_strbool(value):
    return value and 'true' or 'false'


def preprocess_int(integer_string):
    return str(int(integer_string))


def preprocess_list(value):
    if not isinstance(value, list):
        raise ValueError("must be a list")
    return value


def preprocess_ipaddr(ipaddr):
    # TODO: validate the ip address format
    return ipaddr


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

    def accounts_balances(self, accounts):
        """
        Returns how many RAW is owned and how many have not yet been received
        by **accounts list**

        :type accounts: list

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

        accounts = preprocess_list(accounts)

        payload = {
            "accounts": accounts,
        }

        resp = self.call('accounts_balances', payload)
        accounts_balances = resp.get('balances') or {}

        for account, balances in accounts_balances.items():
            for k in balances:
                balances[k] = int(balances[k])

        return accounts_balances

    def account_block_count(self, account):
        """
        Get number of blocks for a specific **account**

        :type account: str

        >>> rpc.account_block_count(account="xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3")
        19

        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('account_block_count', payload)

        return int(resp['block_count'])

    def accounts_create(self, wallet, count):
        """
        Creates new accounts, insert next deterministic keys in **wallet** up
        to **count**

        :type wallet: str
        :type count: int

        .. enable_control required
        .. version 8.0 required

        >>> rpc.accounts_create(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     count=2
        ... )
        [
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
            "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3s00000000"
        ]

        """

        wallet = preprocess_wallet(wallet)
        count = preprocess_int(count)

        payload = {
            "wallet": wallet,
            "count": count,
        }

        resp = self.call('accounts_create', payload)

        return resp.get('accounts') or []

    def accounts_frontiers(self, accounts):
        """
        Returns a list of pairs of account and block hash representing the
        head block for **accounts list**

        :type accounts: list

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

        accounts = preprocess_list(accounts)

        payload = {
            "accounts": accounts,
        }

        resp = self.call('accounts_frontiers', payload)

        return resp['frontiers']

    def account_info(self, account, representative=False, weight=False,
                     pending=False):
        """
        Returns frontier, open block, change representative block, balance,
        last modified timestamp from local database & block count for
        **account**

        :type account: str
        :type representative: bool
        :type weight: bool
        :type pending: bool

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

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        if representative:
            payload['representative'] = preprocess_strbool(representative)
        if weight:
            payload['weight'] = preprocess_strbool(weight)
        if pending:
            payload['pending'] = preprocess_strbool(pending)

        resp = self.call('account_info', payload)

        for key in ('modified_timestamp', 'block_count', 'balance', 'pending', 'weight'):
            if key in resp:
                resp[key] = int(resp[key])

        return resp

    def account_create(self, wallet):
        """
        Creates a new account, insert next deterministic key in **wallet**

        :type wallet: str

        .. enable_control required

        >>> rpc.account_create(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('account_create', payload)

        return resp['account']

    def account_get(self, key):
        """
        Get account number for the **public key**

        :type key: str

        >>> rpc.account_get(
        ...    key="3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"
        ... )
        "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"

        """

        key = preprocess_public_key(key)

        payload = {
            "key": key,
        }

        resp = self.call('account_get', payload)

        return resp['account']

    def account_history(self, account, count):
        """
        Reports send/receive information for a **account**

        :type account: str
        :type count: int

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

        account = preprocess_account(account)
        count = preprocess_int(count)

        payload = {
            "account": account,
            "count": count,
        }

        resp = self.call('account_history', payload)
        history = resp.get('history') or []

        for entry in history:
            entry['amount'] = int(entry['amount'])

        return history

    def account_list(self, wallet):
        """
        Lists all the accounts inside **wallet**

        :type wallet: str

        >>> rpc.account_list(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        [
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ]

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('account_list', payload)

        return resp.get('accounts') or []

    def account_move(self, source, wallet, accounts):
        """
        Moves **accounts** from **source** to **wallet**

        :type wallet: str
        :type source: str
        :type accounts: list

        .. enable_control required

        >>> rpc.account_move(
        ...     source="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     accounts=[
        ...         "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ...     ]
        ... )
        True

        """

        wallet = preprocess_wallet(wallet)
        source = preprocess_wallet(source)
        accounts = preprocess_list(accounts)

        payload = {
            "wallet": wallet,
            "source": source,
            "accounts": accounts,
        }

        resp = self.call('account_move', payload)

        return resp['moved'] == '1'

    def accounts_pending(self, accounts, count=None, threshold=None, source=False):
        """
        Returns a list of block hashes which have not yet been received by
        these **accounts**

        :type accounts: list
        :type count: int
        :type threshold: int
        :type source: bool

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

        accounts = preprocess_list(accounts)
        if count is not None:
            payload['count'] = preprocess_int(count)

        if threshold is not None:
            payload['threshold'] = preprocess_int(threshold)

        if source:
            payload['source'] = preprocess_strbool(source)

        resp = self.call('accounts_pending', payload)

        blocks = resp.get('blocks') or {}
        for account, data in blocks.items():
            if isinstance(data, list):  # list of block hashes
                continue
            for key, value in data.items():
                if isinstance(value, six.string_types):  # amount
                    data[key] = int(value)
                elif isinstance(value, dict):  # dict with "amount" and "source"
                    for key in ('amount',):
                        if key in value:
                            value[key] = int(value[key])

        return resp['blocks'] or {}

    def account_key(self, account):
        """
        Get the public key for **account**

        :type account: str

        >>> rpc.account_key(
        ...     account="xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
        ... )
        "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"

        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('account_key', payload)

        return resp['key']

    def account_remove(self, wallet, account):
        """
        Remove **account** from **wallet**

        :type wallet: str
        :type account: str

        .. enable_control required

        >>> rpc.account_remove(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
        ... )
        True

        """

        wallet = preprocess_wallet(wallet)
        account = preprocess_account(account)

        payload = {
            "wallet": wallet,
            "account": account,
        }

        resp = self.call('account_remove', payload)

        return resp['removed'] == '1'

    def account_representative(self, account):
        """
        Returns the representative for **account**

        :type account: str

        >>> rpc.account_representative(
        ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
        )
        "xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"

        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('account_representative', payload)

        return resp['representative']

    def account_representative_set(self, wallet, account, representative):
        """
        Sets the representative for **account** in **wallet**

        :type wallet: str
        :type account: str
        :type representative: str

        .. enable_control required

        >>> rpc.account_representative_set(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi",
        ...     representative="xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"
        ... )
        "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"

        """

        wallet = preprocess_wallet(wallet)
        account = preprocess_account(account)
        representative = preprocess_account(representative)

        payload = {
            "wallet": wallet,
            "account": account,
            "representative": representative,
        }

        resp = self.call('account_representative_set', payload)

        return resp['block']

    def account_weight(self, account):
        """
        Returns the voting weight for **account**

        :type account: str

        >>> rpc.account_weight(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        10000

        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('account_weight', payload)

        return int(resp['weight'])

    def available_supply(self):
        """
        Returns how many rai are in the public supply

        >>> rpc.available_supply()
        10000

        """

        resp = self.call('available_supply')

        return int(resp['available'])

    def block(self, hash):
        """
        Retrieves a json representation of **block**

        :type hash: str

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

        hash = preprocess_block(hash)

        payload = {
            "hash": hash,
        }

        resp = self.call('block', payload)

        return json.loads(resp['contents'])

    def blocks(self, hashes):
        """
        Retrieves a json representations of **blocks**

        :type hashes: list

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

        hashes = preprocess_list(hashes)

        payload = {
            "hashes": hashes,
        }

        resp = self.call('blocks', payload)
        blocks = resp['blocks'] or {}

        return {
            k: json.loads(v) for k, v in blocks.items()
        }

    def blocks_info(self, hashes, pending=False, source=False):
        """
        Retrieves a json representations of **blocks** with transaction
        **amount** & block **account**

        :type hashes: list
        :type pending: bool
        :type source: bool

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

        hashes = preprocess_list(hashes)

        payload = {
            "hashes": hashes,
        }

        if pending:
            payload['pending'] = preprocess_strbool(pending)
        if source:
            payload['source'] = preprocess_strbool(source)


        resp = self.call('blocks_info', payload)

        blocks = resp.get('blocks') or {}

        for block, data in blocks.items():
            data['contents'] = json.loads(data['contents'])
            for key in ('amount', 'pending'):
                if key in data:
                    data[key] = int(data[key])

        return blocks

    def block_account(self, hash):
        """
        Returns the account containing block

        :type hash: str

        >>> rpc.block_account(
        ...     hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        hash = preprocess_block(hash)

        payload = {
            "hash": hash,
        }

        resp = self.call('block_account', payload)

        return resp['account']

    def block_count(self):
        """
        Reports the number of blocks in the ledger and unchecked synchronizing
        blocks

        >>> rpc.block_count()
        {
          "count": 1000,
          "unchecked": 10
        }

        """

        resp = self.call('block_count')

        return {
            k: int(v) for k, v in resp.items()
        }

    def block_count_type(self):
        """
        Reports the number of blocks in the ledger by type (send, receive,
        open, change)

        >>> rpc.block_count_type()
        {
          "send": 1000,
          "receive": 900,
          "open": 100,
          "change": 50
        }

        """

        resp = self.call('block_count_type')

        return {
            k: int(v) for k, v in resp.items()
        }

    def bootstrap(self, address, port):
        """
        Initialize bootstrap to specific **IP address** and **port**

        :type address: str
        :type port: int

        >>> rpc.bootstrap(address="::ffff:138.201.94.249", port="7075")
        True
        """

        address = preprocess_ipaddr(address)
        port = preprocess_int(port)

        payload = {
            "address": address,
            "port": port,
        }

        resp = self.call('bootstrap', payload)

        return 'success' in resp

    def bootstrap_any(self):
        """
        Initialize multi-connection bootstrap to random peers

        >>> rpc.bootstrap_any()
        True
        """

        resp = self.call('bootstrap_any')

        return 'success' in resp

    def chain(self, block, count):
        """
        Returns a list of block hashes in the account chain starting at
        **block** up to **count**

        :type block: str
        :type count: int

        >>> rpc.chain(
        ...     block="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     count=1
        ... )
        [
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ]

        """

        block = preprocess_block(block)
        count = preprocess_int(count)

        payload = {
            "block": block,
            "count": count,
        }

        resp = self.call('chain', payload)

        return resp.get('blocks') or []

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
