.. _account-ref:

Account
=======

account_balance
---------------

Returns how many RAW is owned and how many have not yet been received by **account**
:py:func:`nano.rpc.Client.account_balance(account) <nano.rpc.Client.account_balance>`

.. .. py:function:: nano.rpc.Client.account_balance(account)

..
   Returns how many RAW is owned and how many have not yet been received
   by **account**

   :param account: Account id to return balance of
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_balance(
   ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
   ... )
   {
     "balance": 10000,
     "pending": 10000
   }


account_block_count
-------------------

Get number of blocks for a specific **account**
:py:func:`nano.rpc.Client.account_block_count(account) <nano.rpc.Client.account_block_count>`

.. .. py:function:: nano.rpc.Client.account_block_count(account)

..
   Get number of blocks for a specific **account**

   :param account: Account to get number of blocks for
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_block_count(account="xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3")
   19


account_create
--------------

Creates a new account, insert next deterministic key in **wallet**
:py:func:`nano.rpc.Client.account_create(wallet, work=True) <nano.rpc.Client.account_create>`

.. .. py:function:: nano.rpc.Client.account_create(wallet, work=True)

..
   Creates a new account, insert next deterministic key in **wallet**

   .. enable_control required

   :param wallet: Wallet to insert new account into
   :type wallet: str

   :param work: If false, disables work generation after creating account
   :type work: bool

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_create(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"


account_get
-----------

Get account number for the **public key**
:py:func:`nano.rpc.Client.account_get(key) <nano.rpc.Client.account_get>`

.. .. py:function:: nano.rpc.Client.account_get(key)

..
   Get account number for the **public key**

   :param key: Public key to get account for
   :type key: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_get(
   ...    key="3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"
   ... )
   "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"


account_history
---------------

Reports send/receive information for a **account**
:py:func:`nano.rpc.Client.account_history(account, count) <nano.rpc.Client.account_history>`

.. .. py:function:: nano.rpc.Client.account_history(account, count)

..
   Reports send/receive information for a **account**

   :param account: Account to get send/receive information for
   :type account: str

   :param count: number of blocks to return
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

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


account_info
------------

Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count for **account**
:py:func:`nano.rpc.Client.account_info(account, representative=False, weight=False, pending=False) <nano.rpc.Client.account_info>`

.. .. py:function:: nano.rpc.Client.account_info(account, representative=False, weight=False, pending=False)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

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


account_key
-----------

Get the public key for **account**
:py:func:`nano.rpc.Client.account_key(account) <nano.rpc.Client.account_key>`

.. .. py:function:: nano.rpc.Client.account_key(account)

..
   Get the public key for **account**

   :param account: Account to get public key for
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_key(
   ...     account="xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
   ... )
   "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"


account_list
------------

Lists all the accounts inside **wallet**
:py:func:`nano.rpc.Client.account_list(wallet) <nano.rpc.Client.account_list>`

.. .. py:function:: nano.rpc.Client.account_list(wallet)

..
   Lists all the accounts inside **wallet**

   :param wallet: Wallet to get account list for
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_list(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   [
       "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
   ]


account_move
------------

Moves **accounts** from **source** to **wallet**
:py:func:`nano.rpc.Client.account_move(source, wallet, accounts) <nano.rpc.Client.account_move>`

.. .. py:function:: nano.rpc.Client.account_move(source, wallet, accounts)

..
   Moves **accounts** from **source** to **wallet**

   .. enable_control required

   :param source: wallet to move accounts from
   :type source: str

   :param wallet: wallet to move accounts to
   :type wallet: str

   :param accounts: accounts to move
   :type accounts: list of str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_move(
   ...     source="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     accounts=[
   ...         "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
   ...     ]
   ... )
   True


account_remove
--------------

Remove **account** from **wallet**
:py:func:`nano.rpc.Client.account_remove(wallet, account) <nano.rpc.Client.account_remove>`

.. .. py:function:: nano.rpc.Client.account_remove(wallet, account)

..
   Remove **account** from **wallet**

   .. enable_control required

   :param wallet: Wallet to remove account from
   :type wallet: str

   :param account: Account to remove
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_remove(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
   ... )
   True


account_representative
----------------------

Returns the representative for **account**
:py:func:`nano.rpc.Client.account_representative(account) <nano.rpc.Client.account_representative>`

.. .. py:function:: nano.rpc.Client.account_representative(account)

..
   Returns the representative for **account**

   :param account: Account to get representative for
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_representative(
   ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
   )
   "xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"


account_representative_set
--------------------------

Sets the representative for **account** in **wallet**
:py:func:`nano.rpc.Client.account_representative_set(wallet, account, representative, work=None) <nano.rpc.Client.account_representative_set>`

.. .. py:function:: nano.rpc.Client.account_representative_set(wallet, account, representative, work=None)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_representative_set(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     account="xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi",
   ...     representative="xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"
   ... )
   "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"


account_weight
--------------

Returns the voting weight for **account**
:py:func:`nano.rpc.Client.account_weight(account) <nano.rpc.Client.account_weight>`

.. .. py:function:: nano.rpc.Client.account_weight(account)

..
   Returns the voting weight for **account**

   :param account: Account to get voting weight for
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.account_weight(
   ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
   ... )
   10000


accounts_balances
-----------------

Returns how many RAW is owned and how many have not yet been received by **accounts** list
:py:func:`nano.rpc.Client.accounts_balances(accounts) <nano.rpc.Client.accounts_balances>`

.. .. py:function:: nano.rpc.Client.accounts_balances(accounts)

..
   Returns how many RAW is owned and how many have not yet been received
   by **accounts** list

   :param accounts: list of accounts to return balances for
   :type accounts: list of str

   :raises: :py:exc:`nano.rpc.RPCException`

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


accounts_create
---------------

Creates new accounts, insert next deterministic keys in **wallet** up to **count**
:py:func:`nano.rpc.Client.accounts_create(wallet, count, work=True) <nano.rpc.Client.accounts_create>`

.. .. py:function:: nano.rpc.Client.accounts_create(wallet, count, work=True)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.accounts_create(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     count=2
   ... )
   [
       "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
       "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3s00000000"
   ]


accounts_frontiers
------------------

Returns a list of pairs of account and block hash representing the head block for **accounts** list
:py:func:`nano.rpc.Client.accounts_frontiers(accounts) <nano.rpc.Client.accounts_frontiers>`

.. .. py:function:: nano.rpc.Client.accounts_frontiers(accounts)

..
   Returns a list of pairs of account and block hash representing the
   head block for **accounts** list

   :param accounts: Accounts to return frontier blocks for
   :type accounts: list of str

   :raises: :py:exc:`nano.rpc.RPCException`

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


accounts_pending
----------------

Returns a list of block hashes which have not yet been received by these **accounts**
:py:func:`nano.rpc.Client.accounts_pending(accounts, count=None, threshold=None, source=False) <nano.rpc.Client.accounts_pending>`

.. .. py:function:: nano.rpc.Client.accounts_pending(accounts, count=None, threshold=None, source=False)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

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


block_account
-------------

Returns the account containing block
:py:func:`nano.rpc.Client.block_account(hash) <nano.rpc.Client.block_account>`

.. .. py:function:: nano.rpc.Client.block_account(hash)

..
   Returns the account containing block

   :param hash: Hash of the block to return account for
   :type hash: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.block_account(
   ...     hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"


delegators
----------

Returns a list of pairs of delegator names given **account** a representative and its balance
:py:func:`nano.rpc.Client.delegators(account) <nano.rpc.Client.delegators>`

.. .. py:function:: nano.rpc.Client.delegators(account)

..
   Returns a list of pairs of delegator names given **account** a
   representative and its balance

   .. version 8.0 required

   :param account: Account to return delegators for
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.delegators(
   ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda"
   ... )
   {
       "xrb_13bqhi1cdqq8yb9szneoc38qk899d58i5rcrgdk5mkdm86hekpoez3zxw5sd":
           "500000000000000000000000000000000000",
       "xrb_17k6ug685154an8gri9whhe5kb5z1mf5w6y39gokc1657sh95fegm8ht1zpn":
           "961647970820730000000000000000000000"
   }


delegators_count
----------------

Get number of delegators for a specific representative **account**
:py:func:`nano.rpc.Client.delegators_count(account) <nano.rpc.Client.delegators_count>`

.. .. py:function:: nano.rpc.Client.delegators_count(account)

..
   Get number of delegators for a specific representative **account**

   .. version 8.0 required

   :param account: Account to get number of delegators for
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.delegators_count(
   ...     account="xrb_1111111111111111111111111111111111111111111111111117353trpda"
   ... )
   2


frontiers
---------

Returns a list of pairs of account and block hash representing the head block starting at **account** up to **count**
:py:func:`nano.rpc.Client.frontiers(account, count) <nano.rpc.Client.frontiers>`

.. .. py:function:: nano.rpc.Client.frontiers(account, count)

..
   Returns a list of pairs of account and block hash representing the
   head block starting at **account** up to **count**

   :param account: Account to get frontier blocks for
   :type account: str

   :param count: Max amount to return
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.frontiers(
   ...     account="xrb_1111111111111111111111111111111111111111111111111111hifc8npp",
   ...     count=1
   ... )
   {
       "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000":
           "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   }


ledger
------

Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count starting at **account** up to **count**
:py:func:`nano.rpc.Client.ledger(account, count=None, representative=False, weight=False, pending=False, sorting=False) <nano.rpc.Client.ledger>`

.. .. py:function:: nano.rpc.Client.ledger(account, count=None, representative=False, weight=False, pending=False, sorting=False)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

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


payment_wait
------------

Wait for payment of **amount** to arrive in **account** or until **timeout** milliseconds have elapsed.
:py:func:`nano.rpc.Client.payment_wait(account, amount, timeout) <nano.rpc.Client.payment_wait>`

.. .. py:function:: nano.rpc.Client.payment_wait(account, amount, timeout)

..
   Wait for payment of **amount** to arrive in **account** or until **timeout**
   milliseconds have elapsed.

   :param account: Account to wait for payment
   :type account: str

   :param amount: Amount in raw of funds to wait for payment to arrive
   :type amount: int

   :param timeout: Timeout in milliseconds to wait for
   :type timeout: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.payment_wait(
   ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
   ...     amount=1,
   ...     timeout=1000
   ... )
   True


pending
-------

Returns a list of pending block hashes with amount more or equal to **threshold**
:py:func:`nano.rpc.Client.pending(account, count=None, threshold=None, source=False) <nano.rpc.Client.pending>`

.. .. py:function:: nano.rpc.Client.pending(account, count=None, threshold=None, source=False)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

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


receive
-------

Receive pending **block** for **account** in **wallet**
:py:func:`nano.rpc.Client.receive(wallet, account, block, work=None) <nano.rpc.Client.receive>`

.. .. py:function:: nano.rpc.Client.receive(wallet, account, block, work=None)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.receive(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
   ...     block="53EAA25CE28FA0E6D55EA9704B32604A736966255948594D55CBB05267CECD48",
   ...     work="12041e830ad10de1"
   ... )
   "EE5286AB32F580AB65FD84A69E107C69FBEB571DEC4D99297E19E3FA5529547B"


send
----

Send **amount** from **source** in **wallet** to **destination**
:py:func:`nano.rpc.Client.send(wallet, source, destination, amount, work=None) <nano.rpc.Client.send>`

.. .. py:function:: nano.rpc.Client.send(wallet, source, destination, amount, work=None)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.send(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     source="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
   ...     destination="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
   ...     amount=1000000,
   ...     work="2bf29ef00786a6bc"
   ... )
   "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"


validate_account_number
-----------------------

Check whether **account** is a valid account number
:py:func:`nano.rpc.Client.validate_account_number(account) <nano.rpc.Client.validate_account_number>`

.. .. py:function:: nano.rpc.Client.validate_account_number(account)

..
   Check whether **account** is a valid account number

   :param account: Account number to check
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.validate_account_number(
   ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
   ... )
   True

