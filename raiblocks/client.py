import six
import json
import requests

from .models import (
    Account, Wallet, PublicKey, Work, PrivateKey, Block, Seed
)


def preprocess_account(account_string):
    return Account(account_string)


def preprocess_wallet(wallet_string):
    return Wallet(wallet_string)


def preprocess_block(block_string):
    return Block(block_string)


def preprocess_seed(seed_string):
    return Seed(seed_string)


def preprocess_public_key(public_key_string):
    return PublicKey(public_key_string)


def preprocess_private_key(private_key_string):
    return PublicKey(private_key_string)


def preprocess_strbool(value):
    return value and 'true' or 'false'


def preprocess_work(work_string):
    return Work(work_string)


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

    def accounts_create(self, wallet, count, work=True):
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

        if not work:
            payload['work'] = preprocess_strbool(work)

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

    def account_create(self, wallet, work=True):
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

        if not work:
            payload['work'] = preprocess_strbool(work)

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

    def account_representative_set(self, wallet, account, representative, work=None):
        """
        Sets the representative for **account** in **wallet**

        :type wallet: str
        :type account: str
        :type representative: str
        :type work: str

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

        if work is not None:
            payload['work'] = preprocess_work(work)

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

    def delegators(self, account):
        """
        Returns a list of pairs of delegator names given **account** a
        representative and its balance

        :type account: str

        .. version 8.0 required

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

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('delegators', payload)

        return resp.get('delegators') or {}

    def delegators_count(self, account):
        """
        Get number of delegators for a specific representative **account**

        :type account: str

        .. version 8.0 required

        >>> rpc.delegators_count(
        ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda"
        ... )
        2

        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('delegators_count', payload)

        return int(resp['count'])

    def deterministic_key(self, seed, index):
        """
        Derive deterministic keypair from **seed** based on **index**

        :type seed: str
        :type index: int

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

        seed = preprocess_seed(seed)
        index = preprocess_int(index)

        payload = {
            "seed": seed,
            "index": index,
        }

        resp = self.call('deterministic_key', payload)

        return resp

    def frontiers(self, account, count):
        """
        Returns a list of pairs of account and block hash representing the
        head block starting at **account** up to **count**

        :type account: str
        :type count: int

        >>> rpc.frontiers(
        ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
        ...     count=1
        ... )
        {
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000":
                "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        }

        """

        account = preprocess_account(account)
        count = preprocess_int(count)

        payload = {
            "account": account,
            "count": count,
        }

        resp = self.call('frontiers', payload)

        return resp.get('frontiers') or {}

    def frontier_count(self):
        """
        Reports the number of accounts in the ledger

        >>> rpc.frontier_count()
        1000

        """

        resp = self.call('frontier_count')

        return int(resp['count'])

    def history(self, hash, count):
        """
        Reports send/receive information for a chain of blocks

        :type hash: str
        :type count: int

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

        hash = preprocess_block(hash)
        count = preprocess_int(count)

        payload = {
            "hash": hash,
            "count": count,
        }

        resp = self.call('history', payload)

        for entry in resp['history']:
            entry['amount'] = int(entry['amount'])

        return resp['history']

    def mrai_from_raw(self, amount):
        """
        Divide a raw amount down by the Mrai ratio.

        :type amount: int

        >>> rpc.mrai_from_raw(amount=1000000000000000000000000000000)
        1

        """

        amount = preprocess_int(amount)

        payload = {
            "amount": amount,
        }

        resp = self.call('mrai_from_raw', payload)

        return int(resp['amount'])

    def mrai_to_raw(self, amount):
        """
        Multiply an Mrai amount by the Mrai ratio.

        :type amount: int

        >>> rpc.mrai_to_raw(amount=1)
        1000000000000000000000000000000

        """

        amount = preprocess_int(amount)

        payload = {
            "amount": amount,
        }

        resp = self.call('mrai_to_raw', payload)

        return int(resp['amount'])

    def krai_from_raw(self, amount):
        """
        Divide a raw amount down by the krai ratio.

        :type amount: int

        >>> rpc.krai_from_raw(amount=1000000000000000000000000000)
        1
        """

        amount = preprocess_int(amount)

        payload = {
            "amount": amount,
        }

        resp = self.call('krai_from_raw', payload)

        return int(resp['amount'])

    def krai_to_raw(self, amount):
        """
        Multiply an krai amount by the krai ratio.

        :type amount: int

        >>> rpc.krai_to_raw(amount=1)
        1000000000000000000000000000

        """

        amount = preprocess_int(amount)

        payload = {
            "amount": amount,
        }

        resp = self.call('krai_to_raw', payload)

        return int(resp['amount'])

    def rai_from_raw(self, amount):
        """
        Divide a raw amount down by the rai ratio.

        :type amount: int

        >>> rpc.rai_from_raw(amount=1000000000000000000000000)
        1

        """

        amount = preprocess_int(amount)

        payload = {
            "amount": amount,
        }

        resp = self.call('rai_from_raw', payload)

        return int(resp['amount'])

    def rai_to_raw(self, amount):
        """
        Multiply an rai amount by the rai ratio.

        :type amount: int

        >>> rpc.rai_to_raw(amount=1)
        1000000000000000000000000

        """

        amount = preprocess_int(amount)

        payload = {
            "amount": amount,
        }

        resp = self.call('rai_to_raw', payload)

        return int(resp['amount'])

    def key_create(self):
        """
        Generates an **adhoc random keypair**

        >>> rpc.key_create()
        {
          "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
          "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
          "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
        }

        """

        resp = self.call('key_create')

        return resp

    def key_expand(self, key):
        """
        Derive public key and account number from **private key**

        :type key: str

        >>> rpc.key_expand(
            key="781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
        )
        {
          "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
          "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
          "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
        }

        """

        key = preprocess_private_key(key)

        payload = {
            "key": key,
        }

        resp = self.call('key_expand', payload)

        return resp

    def keepalive(self, address, port):
        """
        Tells the node to send a keepalive packet to **address**:**port**

        :type address: str
        :type port: int

        .. enable_control required

        >>> rpc.keepalive(address="::ffff:192.168.1.1", port=1024)
        True
        """

        address = preprocess_ipaddr(address)
        port = preprocess_int(port)

        payload = {
            "address": address,
            "port": port,
        }

        resp = self.call('keepalive', payload)

        return resp == {}

    def ledger(self, account, count=None, representative=False, weight=False,
               pending=False):
        """
        Returns frontier, open block, change representative block, balance,
        last modified timestamp from local database & block count starting at
        **account** up to **count**

        :type account: str
        :type count: int
        :type representative: bool
        :type weight: bool
        :type pending: bool

        .. enable_control required
        .. version 8.0 required

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

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        if count is not None:
            payload['count'] = preprocess_int(count)

        if representative:
            payload['representative'] = preprocess_strbool(representative)

        if weight:
            payload['weight'] = preprocess_strbool(weight)

        if pending:
            payload['pending'] = preprocess_strbool(pending)

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

    def payment_begin(self, wallet):
        """
        Begin a new payment session. Searches wallet for an account that's
        marked as available and has a 0 balance. If one is found, the account
        number is returned and is marked as unavailable. If no account is
        found, a new account is created, placed in the wallet, and returned.

        :type wallet: str

        >>> rpc.payment_begin(
        ... wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('payment_begin', payload)

        return resp['account']

    # NOTE(dan): Server RPC is broken here - it *should* return an
    # 'error' for 'No wallet found', but it returns 'status' instead
    # https://github.com/clemahieu/raiblocks/blob/e9592e5/rai/node/rpc.cpp#L2238
    def payment_init(self, wallet):
        """
        Marks all accounts in wallet as available for being used as a payment
        session.

        :type wallet: str

        >>> rpc.payment_init(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True
        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('payment_init', payload)

        return resp['status'] == 'Ready'

    def payment_end(self, account, wallet):
        """
        End a payment session.  Marks the account as available for use in a
        payment session.

        :type account: str
        :type wallet: str

        >>> rpc.payment_end(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     wallet="FFFD1BAEC8EC20814BBB9059B393051AAA8380F9B5A2E6B2489A277D81789EEE"
        ... )
        True
        """

        account = preprocess_account(account)
        wallet = preprocess_wallet(wallet)

        payload = {
            "account": account,
            "wallet": wallet,
        }

        resp = self.call('payment_end', payload)

        return resp == {}

    def payment_wait(self, account, amount, timeout):
        """
        Wait for payment of 'amount' to arrive in 'account' or until 'timeout'
        milliseconds have elapsed.

        :type account: str
        :type amount: int
        :type timeout: int

        >>> rpc.payment_wait(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     amount=1,
        ...     timeout=1000
        ... )
        True

        """

        account = preprocess_account(account)
        amount = preprocess_int(amount)
        timeout = preprocess_int(timeout)

        payload = {
            "account": account,
            "amount": amount,
            "timeout": timeout,
        }

        resp = self.call('payment_wait', payload)

        return resp['status'] == 'success'

    def process(self, block):
        """
        Publish **block** to the network

        :type block: dict or json

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

        def _preprocess_json_dict(value):
            if isinstance(value, dict):
                return json.dumps(value, sort_keys=True)
            return value


        block = _preprocess_json_dict(block)

        payload = {
            "block": block,
        }

        resp = self.call('process', payload)

        return resp['hash']

    def receive(self, wallet, account, block, work=None):
        """
        Receive pending **block** for **account** in **wallet**

        :type wallet: str
        :type account: str
        :type block: str
        :type work: str

        .. enable_control required

        >>> rpc.receive(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     block="53EAA25CE28FA0E6D55EA9704B32604A736966255948594D55CBB05267CECD48",
        ...     work="12041e830ad10de1"
        ... )
        "EE5286AB32F580AB65FD84A69E107C69FBEB571DEC4D99297E19E3FA5529547B"

        """

        wallet = preprocess_wallet(wallet)
        account = preprocess_account(account)
        block = preprocess_block(block)

        payload = {
            "wallet": wallet,
            "account": account,
            "block": block,
        }

        if work:
            payload['work'] = preprocess_work(work)

        resp = self.call('receive', payload)

        return resp['block']

    def receive_minimum(self):
        """
        Returns receive minimum for node

        .. enable_control required
        .. version 8.0 required

        >>> rpc.receive_minimum()
        1000000000000000000000000

        """

        resp = self.call('receive_minimum')

        return int(resp['amount'])

    def receive_minimum_set(self, amount):
        """
        Set **amount** as new receive minimum for node until restart

        :type amount: int

        .. enable_control required
        .. version 8.0 required

        >>> rpc.receive_minimum_set(amount=1000000000000000000000000000000)
        True
        """

        amount = preprocess_int(amount)

        payload = {
            "amount": amount,
        }

        resp = self.call('receive_minimum_set', payload)

        return 'success' in resp

    def representatives(self):
        """
        Returns a list of pairs of representative and its voting weight

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

        resp = self.call('representatives')
        representatives = resp.get('representatives') or {}

        return {
            k: int(v) for k, v in representatives.items()
        }

    def unchecked(self, count=None):
        """
        Returns a list of pairs of unchecked synchronizing block hash and its
        json representation up to **count**

        :type count: int

        .. version 8.0 required

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
            payload["count"] = preprocess_int(count)

        resp = self.call('unchecked', payload)

        blocks = resp.get('blocks') or {}
        for block, block_json in blocks.items():
            blocks[block] = json.loads(block_json)

        return blocks

    def unchecked_clear(self):
        """
        Clear unchecked synchronizing blocks

        .. enable_control required
        .. version 8.0 required

        >>> rpc.unchecked_clear()
        True

        """

        resp = self.call('unchecked_clear')

        return 'success' in resp

    def unchecked_get(self, hash):
        """
        Retrieves a json representation of unchecked synchronizing block by
        **hash**

        :type hash: str

        .. version 8.0 required

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

        hash = preprocess_block(hash)

        payload = {
            "hash": hash,
        }

        resp = self.call('unchecked_get', payload)

        return json.loads(resp['contents'])

    def unchecked_keys(self, key, count=None):
        """
        Retrieves unchecked database keys, blocks hashes & a json
        representations of unchecked pending blocks starting from **key** up
        to **count**

        :type key: str
        :type count: int

        .. version 8.0 required

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

        key = preprocess_public_key(key)

        payload = {
            "key": key,
        }

        if count is not None:
            payload['count'] = preprocess_int(count)

        resp = self.call('unchecked_keys', payload)
        unchecked = resp.get('unchecked') or []

        for entry in unchecked:
            entry['contents'] = json.loads(entry['contents'])

        return unchecked

    def validate_account_number(self, account):
        """
        Check whether **account** is a valid account number

        :type account: str

        >>> rpc.validate_account_number(
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        True
        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        resp = self.call('validate_account_number', payload)

        return resp['valid'] == '1'

    def wallet_representative(self, wallet):
        """
        Returns the default representative for **wallet**

        :type wallet: str

        >>> rpc.wallet_representative(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_representative', payload)

        return resp['representative']

    def wallet_representative_set(self, wallet, representative):
        """
        Sets the default **representative** for **wallet**

        :type wallet: str
        :type representative: str

        .. enable_control required

        >>> rpc.wallet_representative_set(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     representative="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        True

        """

        wallet = preprocess_wallet(wallet)
        representative = preprocess_account(representative)

        payload = {
            "wallet": wallet,
            "representative": representative,
        }

        resp = self.call('wallet_representative_set', payload)

        return resp['set'] == '1'

    def wallet_add(self, wallet, key, work=True):
        """
        Add an adhoc private key **key** to **wallet**

        :type wallet: str
        :type key: str

        .. enable_control required

        >>> rpc.wallet_add(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     key="34F0A37AAD20F4A260F0A5B3CB3D7FB50673212263E58A380BC10474BB039CE4"
        ... )
        "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"

        """

        wallet = preprocess_wallet(wallet)
        key = preprocess_private_key(key)

        payload = {
            "wallet": wallet,
            "key": key,
        }

        if not work:
            payload['work'] = preprocess_strbool(work)

        resp = self.call('wallet_add', payload)

        return resp['account']

    def wallet_balance_total(self, wallet):
        """
        Returns the sum of all accounts balances in **wallet**

        :type wallet: str

        >>> rpc.wallet_balance_total(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
          "balance": 10000,
          "pending": 10000
        }

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_balance_total', payload)

        return {
            k: int(v) for k, v in resp.items()
        }

    def wallet_balances(self, wallet):
        """
        Returns how many rai is owned and how many have not yet been received
        by all accounts in **wallet**

        :type wallet: str

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

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_balances', payload)
        balances = resp.get('balances') or {}
        for account, balance in balances.items():
            balances[account] = {
                k: int(v) for k, v in balances[account].items()
            }

        return balances

    def wallet_change_seed(self, wallet, seed):
        """
        Changes seed for **wallet** to **seed**

        :type wallet: str
        :type seed: str

        .. enable_control required

        >>> rpc.wallet_change_seed(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     seed="74F2B37AAD20F4A260F0A5B3CB3D7FB51673212263E58A380BC10474BB039CEE"
        ... )
        True
        """

        wallet = preprocess_wallet(wallet)
        seed = preprocess_seed(seed)

        payload = {
            "wallet": wallet,
            "seed": seed,
        }

        resp = self.call('wallet_change_seed', payload)

        return 'success' in resp

    def wallet_contains(self, wallet, account):
        """
        Check whether **wallet** contains **account**

        :type wallet: str
        :type account: str

        >>> rpc.wallet_contains(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
        ... )
        True
        """

        wallet = preprocess_wallet(wallet)
        account = preprocess_account(account)

        payload = {
            "wallet": wallet,
            "account": account,
        }

        resp = self.call('wallet_contains', payload)

        return resp['exists'] == '1'

    def wallet_create(self):
        """
        Creates a new random wallet id

        .. enable_control required

        >>> rpc.wallet_create()
        "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"

        """

        resp = self.call('wallet_create')

        return resp['wallet']

    def wallet_destroy(self, wallet):
        """
        Destroys **wallet** and all contained accounts

        :type wallet: str

        .. enable_control required

        >>> rpc.wallet_destroy(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True
        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_destroy', payload)

        return resp == {}

    def wallet_export(self, wallet):
        """
        Return a json representation of **wallet**

        :type wallet: str

        >>> rpc.wallet_export(wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F")
        {
            "0000000000000000000000000000000000000000000000000000000000000000": "0000000000000000000000000000000000000000000000000000000000000001"
        }
        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_export', payload)

        return json.loads(resp['json'])

    def wallet_frontiers(self, wallet):
        """
        Returns a list of pairs of account and block hash representing the
        head block starting for accounts from **wallet**

        :type wallet: str

        >>> rpc.wallet_frontiers(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
            "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        }

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_frontiers', payload)

        return resp['frontiers']

    def wallet_locked(self, wallet):
        """
        Checks whether **wallet** is locked

        :type wallet: str

        >>> rpc.wallet_locked(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        False
        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_locked', payload)

        return resp['locked'] == '1'

    def wallet_pending(self, wallet, count=None, threshold=None, source=False):
        """
        Returns a list of block hashes which have not yet been received by
        accounts in this **wallet**

        :type wallet: str
        :type count: int
        :type threshold: int
        :type source: bool

        .. enable_control required
        .. version 8.0 required

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

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        if count is not None:
            payload['count'] = preprocess_int(count)

        if threshold is not None:
            payload['threshold'] = preprocess_int(threshold)

        if source:
            payload['source'] = preprocess_strbool(source)

        resp = self.call('wallet_pending', payload)

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

    def wallet_republish(self, wallet, count):
        """
        Rebroadcast blocks for accounts from **wallet** starting at frontier
        down to **count** to the network

        :type wallet: str
        :type count: int

        .. enable_control required
        .. version 8.0 required

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

        wallet = preprocess_wallet(wallet)
        count = preprocess_int(count)

        payload = {
            "wallet": wallet,
            "count": count,
        }

        resp = self.call('wallet_republish', payload)

        return resp.get('blocks') or []

    def wallet_work_get(self, wallet):
        """
        Returns a list of pairs of account and work from **wallet**

        :type wallet: str

        .. enable_control required
        .. version 8.0 required

        >>> rpc.wallet_work_get(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        {
            "xrb_1111111111111111111111111111111111111111111111111111hifc8npp":
                "432e5cf728c90f4f"
        }

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('wallet_work_get', payload)

        return resp.get('works') or {}

    def password_change(self, wallet, password):
        """
        Changes the password for **wallet** to **password**

        :type wallet: str
        :type password: str

        .. enable_control required

        >>> rpc.password_change(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     password="test"
        ... )
        True
        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
            "password": password,
        }

        resp = self.call('password_change', payload)

        return resp['changed'] == '1'

    def password_enter(self, wallet, password):
        """
        Enters the **password** in to **wallet**

        :type wallet: str
        :type password: str

        >>> rpc.password_enter(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     password="test"
        ... )
        True

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
            "password": password,
        }

        resp = self.call('password_enter', payload)

        return resp['valid'] == '1'

    def password_valid(self, wallet):
        """
        Checks whether the password entered for **wallet** is valid

        :type wallet: str

        >>> rpc.password_valid(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('password_valid', payload)

        return resp['valid'] == '1'

    def peers(self):
        """
        Returns a list of pairs of peer IPv6:port and its node network version

        >>> rpc.peers()
        {
            "[::ffff:172.17.0.1]:32841": 3
        }
        """

        resp = self.call('peers')

        return {
            host: int(version)
            for host, version
            in resp['peers'].items()
        }

    def pending(self, account, count=None, threshold=None, source=False):
        """
        Returns a list of pending block hashes with amount more or equal to
        **threshold**

        :type account: str
        :type count: int
        :type threshold: int
        :type source: bool

        .. version 8.0 required

        >>> rpc.pending(
        ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda",
        ...     count=1,
        ...     threshold=1000000000000000000000000
        ... )
        {
            "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F": "6000000000000000000000000000000"
        }

        """

        account = preprocess_account(account)

        payload = {
            "account": account,
        }

        if count is not None:
            payload['count'] = preprocess_int(count)

        if threshold is not None:
            payload['threshold'] = preprocess_int(threshold)

        if source:
            payload['source'] = preprocess_strbool(source)

        resp = self.call('pending', payload)

        blocks = resp['blocks'] or {}

        for block, value in blocks.items():
            if isinstance(value, six.string_types):  # amount
                blocks[block] = int(value)
            elif isinstance(value, dict):  # dict with "amount" and "source"
                for key in ('amount',):
                    if key in value:
                        value[key] = int(value[key])

        return blocks

    def pending_exists(self, hash):
        """
        Check whether block is pending by **hash**

        :type hash: str

        .. version 8.0 required

        >>> rpc.pending_exists(
            hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        )
        True
        """

        hash = preprocess_block(hash)

        payload = {
            "hash": hash,
        }

        resp = self.call('pending_exists', payload)

        return resp['exists'] == '1'

    def work_cancel(self, hash):
        """
        Stop generating **work** for block

        :type hash: str

        .. enable_control required

        >>> rpc.work_cancel(
        ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
        ... )
        True

        """

        hash = preprocess_block(hash)

        payload = {
            "hash": hash,
        }

        resp = self.call('work_cancel', payload)
        return resp == {}

    def work_generate(self, hash):
        """
        Generates **work** for block

        :type hash: str

        .. enable_control required

        >>> rpc.work_generate(
        ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
        ... )
        "2bf29ef00786a6bc"

        """

        hash = preprocess_block(hash)

        payload = {
            "hash": hash,
        }

        resp = self.call('work_generate', payload)

        return resp['work']

    def work_get(self, wallet, account):
        """
        Retrieves work for **account** in **wallet**

        :type wallet: str
        :type account: str

        .. enable_control required
        .. version 8.0 required

        >>> rpc.work_get(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp"
        ... )
        "432e5cf728c90f4f"

        """

        wallet = preprocess_wallet(wallet)
        account = preprocess_account(account)

        payload = {
            "wallet": wallet,
            "account": account,
        }

        resp = self.call('work_get', payload)

        return resp['work']

    def work_set(self, wallet, account, work):
        """
        Set **work** for **account** in **wallet**

        :type wallet: str
        :type account: str
        :type work: int

        .. enable_control required
        .. version 8.0 required

        >>> rpc.work_set(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
        ...     work="0000000000000000"
        ... )
        True
        """

        wallet = preprocess_wallet(wallet)
        account = preprocess_account(account)
        work = preprocess_work(work)

        payload = {
            "wallet": wallet,
            "account": account,
            "work": work,
        }

        resp = self.call('work_set', payload)

        return 'success' in resp

    def work_peer_add(self, address, port):
        """
        Add specific **IP address** and **port** as work peer for node until
        restart

        :type address: str
        :type port: int

        .. enable_control required
        .. version 8.0 required

        >>> rpc.work_peer_add(address="::ffff:172.17.0.1", port="7076")
        True

        """

        address = preprocess_ipaddr(address)
        port = preprocess_int(port)

        payload = {
            "address": address,
            "port": port,
        }

        resp = self.call('work_peer_add', payload)

        return 'success' in resp

    def work_peers(self):
        """
        Retrieve work peers

        .. enable_control required
        .. version 8.0 required

        >>> rpc.work_peers()
        [
            "::ffff:172.17.0.1:7076"
        ]

        """

        resp = self.call('work_peers')

        return resp['work_peers']

    def work_peers_clear(self):
        """
        Clear work peers node list until restart

        .. enable_control required
        .. version 8.0 required

        >>> rpc.work_peers_clear()
        True

        """

        resp = self.call('work_peers_clear')
        return 'success' in resp

    def work_validate(self, work, hash):
        """
        Check whether **work** is valid for block

        :type work: str
        :type hash: str

        >>> rpc.work_validate(
        ...     work="2bf29ef00786a6bc",
        ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
        ... )
        True

        """

        work = preprocess_work(work)
        hash = preprocess_block(hash)

        payload = {
            "work": work,
            "hash": hash,
        }

        resp = self.call('work_validate', payload)

        return resp['valid'] == '1'

    def republish(self, hash, count=None, sources=None, destinations=None):
        """
        Rebroadcast blocks starting at **hash** to the network

        :type hash: str
        :type count: int
        :type sources: int
        :type destinations: int

        >>> rpc.republish(
        ...     hash="991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"
        ... )
        [
            "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
            "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
        ]

        """

        hash = preprocess_block(hash)

        payload = {
            "hash": hash,
        }

        if count is not None:
            payload['count'] = preprocess_int(count)

        if sources is not None:
            payload['sources'] = preprocess_int(sources)

        if destinations is not None:
            payload['destinations'] = preprocess_int(destinations)

        resp = self.call('republish', payload)

        return resp.get('blocks') or []

    def search_pending(self, wallet):
        """
        Tells the node to look for pending blocks for any account in
        **wallet**

        :type wallet: str

        .. enable_control required

        >>> rpc.search_pending(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
        ... )
        True

        """

        wallet = preprocess_wallet(wallet)

        payload = {
            "wallet": wallet,
        }

        resp = self.call('search_pending', payload)

        return resp['started'] == '1'

    def search_pending_all(self):
        """
        Tells the node to look for pending blocks for any account in all
        available wallets

        .. enable_control required
        .. version 8.0 required

        >>> rpc.search_pending_all()
        True

        """

        resp = self.call('search_pending_all')

        return 'success' in resp

    def send(self, wallet, source, destination, amount, work=None):
        """
        Send **amount** from **source** in **wallet** to **destination**

        :type wallet: str
        :type source: str
        :type destination: str
        :type amount: int
        :type work: str

        .. enable_control required

        >>> rpc.send(
        ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
        ...     source="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     destination="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
        ...     amount=1000000,
        ...     work="2bf29ef00786a6bc"
        ... )
        "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"

        """

        wallet = preprocess_wallet(wallet)
        source = preprocess_account(source)
        destination = preprocess_account(destination)
        amount = preprocess_int(amount)

        payload = {
            "wallet": wallet,
            "source": source,
            "destination": destination,
            "amount": amount,
        }

        if work is not None:
            payload['work'] = preprocess_work(work)

        resp = self.call('send', payload)

        return resp['block']

    def successors(self, block, count):
        """
        Returns a list of block hashes in the account chain ending at
        **block** up to **count**

        :type block: str
        :type count: int

        >>> rpc.successors(
        ...     block="991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
        ...     count=1
        ... )
        [
            "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
        ]

        """

        block = preprocess_block(block)
        count = preprocess_int(count)

        payload = {
            "block": block,
            "count": count,
        }

        resp = self.call('successors', payload)

        return resp.get('blocks') or []

    def stop(self):
        """
        Stop the node

        .. enable_control required

        >>> rpc.stop()
        True

        """

        resp = self.call('stop')

        return 'success' in resp

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
