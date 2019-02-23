.. _wallet-ref:

Wallet
======

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


password_change
---------------

Changes the password for **wallet** to **password**
:py:func:`nano.rpc.Client.password_change(wallet, password) <nano.rpc.Client.password_change>`

.. .. py:function:: nano.rpc.Client.password_change(wallet, password)

..
   Changes the password for **wallet** to **password**

   .. enable_control required

   :param wallet: Wallet to change password for
   :type wallet: str

   :param password: Password to set
   :type password: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.password_change(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     password="test"
   ... )
   True

password_enter
--------------

Enters the **password** in to **wallet**
:py:func:`nano.rpc.Client.password_enter(wallet, password) <nano.rpc.Client.password_enter>`

.. .. py:function:: nano.rpc.Client.password_enter(wallet, password)

..
   Enters the **password** in to **wallet**

   :param wallet: Wallet to enter password for
   :type wallet: str

   :param password: Password to enter
   :type password: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.password_enter(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     password="test"
   ... )
   True


password_valid
--------------

Checks whether the password entered for **wallet** is valid
:py:func:`nano.rpc.Client.password_valid(wallet) <nano.rpc.Client.password_valid>`

.. .. py:function:: nano.rpc.Client.password_valid(wallet)

..
   Checks whether the password entered for **wallet** is valid

   :param wallet: Wallet to check password for
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.password_valid(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   True


payment_begin
-------------

Begin a new payment session. Searches wallet for an account that's marked as available and has a 0 balance. If one is found, the account number is returned and is marked as unavailable. If no account is found, a new account is created, placed in the wallet, and returned.
:py:func:`nano.rpc.Client.payment_begin(wallet) <nano.rpc.Client.payment_begin>`

.. .. py:function:: nano.rpc.Client.payment_begin(wallet)

..
   Begin a new payment session. Searches wallet for an account that's
   marked as available and has a 0 balance. If one is found, the account
   number is returned and is marked as unavailable. If no account is
   found, a new account is created, placed in the wallet, and returned.

   :param wallet: Wallet to begin payment in
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.payment_begin(
   ... wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"


payment_end
-----------

End a payment session.  Marks the account as available for use in a payment session.
:py:func:`nano.rpc.Client.payment_end(account, wallet) <nano.rpc.Client.payment_end>`

.. .. py:function:: nano.rpc.Client.payment_end(account, wallet)

..
   End a payment session.  Marks the account as available for use in a
   payment session.

   :param account: Account to mark available
   :type account: str

   :param wallet: Wallet to end payment session for
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.payment_end(
   ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
   ...     wallet="FFFD1BAEC8EC20814BBB9059B393051AAA8380F9B5A2E6B2489A277D81789EEE"
   ... )
   True

payment_init
------------

Marks all accounts in wallet as available for being used as a payment session.
:py:func:`nano.rpc.Client.payment_init(wallet) <nano.rpc.Client.payment_init>`

.. .. py:function:: nano.rpc.Client.payment_init(wallet)

..
   Marks all accounts in wallet as available for being used as a payment
   session.

   :param wallet: Wallet to init payment in
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.payment_init(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   True

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


search_pending
--------------

Tells the node to look for pending blocks for any account in **wallet**
:py:func:`nano.rpc.Client.search_pending(wallet) <nano.rpc.Client.search_pending>`

.. .. py:function:: nano.rpc.Client.search_pending(wallet)

..
   Tells the node to look for pending blocks for any account in
   **wallet**

   .. enable_control required

   :param wallet: Wallet to search for pending blocks
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.search_pending(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   True


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


wallet_add
----------

Add an adhoc private key **key** to **wallet**
:py:func:`nano.rpc.Client.wallet_add(wallet, key, work=True) <nano.rpc.Client.wallet_add>`

.. .. py:function:: nano.rpc.Client.wallet_add(wallet, key, work=True)

..
   Add an adhoc private key **key** to **wallet**

   .. enable_control required

   :param wallet: Wallet to add private key to
   :type wallet: str

   :param key: Private key to add
   :type key: str

   :param work: If false, disables work generation
   :type work: bool

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_add(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     key="34F0A37AAD20F4A260F0A5B3CB3D7FB50673212263E58A380BC10474BB039CE4"
   ... )
   "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"


wallet_balance_total
--------------------

Returns the sum of all accounts balances in **wallet**
:py:func:`nano.rpc.Client.wallet_balance_total(wallet) <nano.rpc.Client.wallet_balance_total>`

.. .. py:function:: nano.rpc.Client.wallet_balance_total(wallet)

..
   Returns the sum of all accounts balances in **wallet**

   :param wallet: Wallet to return sum of balances for
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_balance_total(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   {
     "balance": 10000,
     "pending": 10000
   }


wallet_balances
---------------

Returns how many rai is owned and how many have not yet been received by all accounts in **wallet**
:py:func:`nano.rpc.Client.wallet_balances(wallet) <nano.rpc.Client.wallet_balances>`

.. .. py:function:: nano.rpc.Client.wallet_balances(wallet)

..
   Returns how many rai is owned and how many have not yet been received
   by all accounts in **wallet**

   :param wallet: Wallet to return balances for
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_balances(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   {
       "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": {
           "balance": 10000,
           "pending": 10000
       }
   }


wallet_change_seed
------------------

Changes seed for **wallet** to **seed**
:py:func:`nano.rpc.Client.wallet_change_seed(wallet, seed) <nano.rpc.Client.wallet_change_seed>`

.. .. py:function:: nano.rpc.Client.wallet_change_seed(wallet, seed)

..
   Changes seed for **wallet** to **seed**

   .. enable_control required

   :param wallet: Wallet to change seed for
   :type wallet: str

   :param seed: Seed to change wallet to
   :type seed: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_change_seed(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     seed="74F2B37AAD20F4A260F0A5B3CB3D7FB51673212263E58A380BC10474BB039CEE"
   ... )
   True

wallet_contains
---------------

Check whether **wallet** contains **account**
:py:func:`nano.rpc.Client.wallet_contains(wallet, account) <nano.rpc.Client.wallet_contains>`

.. .. py:function:: nano.rpc.Client.wallet_contains(wallet, account)

..
   Check whether **wallet** contains **account**

   :param wallet: Wallet to check contains **account**
   :type wallet: str

   :param account: Account to check exists in **wallet**
   :type account: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_contains(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     account="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
   ... )
   True

wallet_create
-------------

Creates a new random wallet id
:py:func:`nano.rpc.Client.wallet_create() <nano.rpc.Client.wallet_create>`

.. .. py:function:: nano.rpc.Client.wallet_create()

..
   Creates a new random wallet id

   .. enable_control required

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_create()
   "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"


wallet_destroy
--------------

Destroys **wallet** and all contained accounts
:py:func:`nano.rpc.Client.wallet_destroy(wallet) <nano.rpc.Client.wallet_destroy>`

.. .. py:function:: nano.rpc.Client.wallet_destroy(wallet)

..
   Destroys **wallet** and all contained accounts

   .. enable_control required

   :param wallet: Wallet to destroy
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_destroy(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   True

wallet_export
-------------

Return a json representation of **wallet**
:py:func:`nano.rpc.Client.wallet_export(wallet) <nano.rpc.Client.wallet_export>`

.. .. py:function:: nano.rpc.Client.wallet_export(wallet)

..
   Return a json representation of **wallet**

   :param wallet: Wallet to export
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_export(wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F")
   {
       "0000000000000000000000000000000000000000000000000000000000000000": "0000000000000000000000000000000000000000000000000000000000000001"
   }

wallet_frontiers
----------------

Returns a list of pairs of account and block hash representing the head block starting for accounts from **wallet**
:py:func:`nano.rpc.Client.wallet_frontiers(wallet) <nano.rpc.Client.wallet_frontiers>`

.. .. py:function:: nano.rpc.Client.wallet_frontiers(wallet)

..
   Returns a list of pairs of account and block hash representing the
   head block starting for accounts from **wallet**

   :param wallet: Wallet to return frontiers for
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_frontiers(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   {
       "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   }


wallet_key_valid
----------------

Returns if a **wallet** key is valid
:py:func:`nano.rpc.Client.wallet_key_valid(wallet) <nano.rpc.Client.wallet_key_valid>`

.. .. py:function:: nano.rpc.Client.wallet_key_valid(wallet)

..
   Returns if a **wallet** key is valid

   :param wallet: Wallet to check key is valid
   :type wallet: str

   >>> rpc.wallet_key_valid(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   True

wallet_lock
-----------

Locks a **wallet**
:py:func:`nano.rpc.Client.wallet_lock(wallet) <nano.rpc.Client.wallet_lock>`

.. .. py:function:: nano.rpc.Client.wallet_lock(wallet)

..
   Locks a **wallet**

   :param wallet: Wallet to lock
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_lock(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   True

wallet_locked
-------------

Checks whether **wallet** is locked
:py:func:`nano.rpc.Client.wallet_locked(wallet) <nano.rpc.Client.wallet_locked>`

.. .. py:function:: nano.rpc.Client.wallet_locked(wallet)

..
   Checks whether **wallet** is locked

   :param wallet: Wallet to check if locked
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_locked(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   False

wallet_pending
--------------

Returns a list of block hashes which have not yet been received by accounts in this **wallet**
:py:func:`nano.rpc.Client.wallet_pending(wallet, count=None, threshold=None, source=False) <nano.rpc.Client.wallet_pending>`

.. .. py:function:: nano.rpc.Client.wallet_pending(wallet, count=None, threshold=None, source=False)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

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


wallet_representative
---------------------

Returns the default representative for **wallet**
:py:func:`nano.rpc.Client.wallet_representative(wallet) <nano.rpc.Client.wallet_representative>`

.. .. py:function:: nano.rpc.Client.wallet_representative(wallet)

..
   Returns the default representative for **wallet**

   :param wallet: Wallet to get default representative account for
   :type wallet: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_representative(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ... )
   "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"


wallet_representative_set
-------------------------

Sets the default **representative** for **wallet**
:py:func:`nano.rpc.Client.wallet_representative_set(wallet, representative) <nano.rpc.Client.wallet_representative_set>`

.. .. py:function:: nano.rpc.Client.wallet_representative_set(wallet, representative)

..
   Sets the default **representative** for **wallet**

   .. enable_control required

   :param wallet: Wallet to set default representative account for
   :type wallet: str

   :param representative: Representative account to set for **wallet**
   :type representative: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_representative_set(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     representative="xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
   ... )
   True


wallet_republish
----------------

Rebroadcast blocks for accounts from **wallet** starting at frontier down to **count** to the network
:py:func:`nano.rpc.Client.wallet_republish(wallet, count) <nano.rpc.Client.wallet_republish>`

.. .. py:function:: nano.rpc.Client.wallet_republish(wallet, count)

..
   Rebroadcast blocks for accounts from **wallet** starting at frontier
   down to **count** to the network

   .. enable_control required
.. version 8.0 required

   :param wallet: Wallet to rebroadcast blocks for
   :type wallet: str

   :param count: Max amount of blocks to rebroadcast since frontier block
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_republish(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     count=2
   ... )
   [
       "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
       "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293",
       "90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35"
   ]


wallet_unlock
-------------

Unlocks **wallet** using **password**
:py:func:`nano.rpc.Client.wallet_unlock(wallet, password) <nano.rpc.Client.wallet_unlock>`

.. .. py:function:: nano.rpc.Client.wallet_unlock(wallet, password)

..
   Unlocks **wallet** using **password**

   :param wallet: Wallet to unlock
   :type wallet: str

   :param password: Password to enter
   :type password: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.wallet_unlock(
   ...     wallet="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     password="test"
   ... )
   True


