.. _block-ref:

Block
=====

block
-----

Retrieves a json representation of **block**
:py:func:`nano.rpc.Client.block(hash) <nano.rpc.Client.block>`

.. .. py:function:: nano.rpc.Client.block(hash)

..
   Retrieves a json representation of **block**

   :param hash: Hash of block to return representation for
   :type hash: str

   :raises: :py:exc:`nano.rpc.RPCException`

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


block_count
-----------

Reports the number of blocks in the ledger and unchecked synchronizing blocks
:py:func:`nano.rpc.Client.block_count() <nano.rpc.Client.block_count>`

.. .. py:function:: nano.rpc.Client.block_count()

..
   Reports the number of blocks in the ledger and unchecked synchronizing
   blocks

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.block_count()
   {
     "count": 1000,
     "unchecked": 10
   }


block_count_type
----------------

Reports the number of blocks in the ledger by type (send, receive, open, change)
:py:func:`nano.rpc.Client.block_count_type() <nano.rpc.Client.block_count_type>`

.. .. py:function:: nano.rpc.Client.block_count_type()

..
   Reports the number of blocks in the ledger by type (send, receive,
   open, change)

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.block_count_type()
   {
     "send": 1000,
     "receive": 900,
     "open": 100,
     "change": 50
   }


block_create
------------

Creates a json representations of new block based on input data & signed with private key or account in **wallet** for offline signing
:py:func:`nano.rpc.Client.block_create(type, account, wallet=None, representative=None, key=None, destination=None, amount=None, balance=None, previous=None, source=None, work=None) <nano.rpc.Client.block_create>`

.. .. py:function:: nano.rpc.Client.block_create(type, account, wallet=None, representative=None, key=None, destination=None, amount=None, balance=None, previous=None, source=None, work=None)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

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

blocks
------

Retrieves a json representations of **blocks**
:py:func:`nano.rpc.Client.blocks(hashes) <nano.rpc.Client.blocks>`

.. .. py:function:: nano.rpc.Client.blocks(hashes)

..
   Retrieves a json representations of **blocks**

   :param hashes: List of block hashes to return
   :type hashes: list of str

   :raises: :py:exc:`nano.rpc.RPCException`

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


blocks_info
-----------

Retrieves a json representations of **blocks** with transaction **amount** & block **account**
:py:func:`nano.rpc.Client.blocks_info(hashes, pending=False, source=False) <nano.rpc.Client.blocks_info>`

.. .. py:function:: nano.rpc.Client.blocks_info(hashes, pending=False, source=False)

..
   Retrieves a json representations of **blocks** with transaction
   **amount** & block **account**

   :param hashes: List of block hashes to return info for
   :type hashes: list of str

   :param pending: If true, returns pending amount as well
   :type pending: bool

   :param source: If true, returns source account as well
   :type source: bool

   :raises: :py:exc:`nano.rpc.RPCException`

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


chain
-----

Returns a list of block hashes in the account chain starting at **block** up to **count**
:py:func:`nano.rpc.Client.chain(block, count) <nano.rpc.Client.chain>`

.. .. py:function:: nano.rpc.Client.chain(block, count)

..
   Returns a list of block hashes in the account chain starting at
   **block** up to **count**

   :param block: Block hash to start at
   :type block: str

   :param count: Number of blocks to return up to
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.chain(
   ...     block="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
   ...     count=1
   ... )
   [
       "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   ]


history
-------

Reports send/receive information for a chain of blocks
:py:func:`nano.rpc.Client.history(hash, count) <nano.rpc.Client.history>`

.. .. py:function:: nano.rpc.Client.history(hash, count)

..
   Reports send/receive information for a chain of blocks

   :param hash: Hash of block to receive history for
   :type hash: str

   :param count: Max number of blocks to return
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

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


pending_exists
--------------

Check whether block is pending by **hash**
:py:func:`nano.rpc.Client.pending_exists(hash) <nano.rpc.Client.pending_exists>`

.. .. py:function:: nano.rpc.Client.pending_exists(hash)

..
   Check whether block is pending by **hash**

   .. version 8.0 required

   :param hash: Hash of block to check if pending
   :type hash: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.pending_exists(
       hash="000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
   )
   True

process
-------

Publish **block** to the network
:py:func:`nano.rpc.Client.process(block) <nano.rpc.Client.process>`

.. .. py:function:: nano.rpc.Client.process(block)

..
   Publish **block** to the network

   :param block: Block to publish
   :type block: dict or json

   :raises: :py:exc:`nano.rpc.RPCException`

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


republish
---------

Rebroadcast blocks starting at **hash** to the network
:py:func:`nano.rpc.Client.republish(hash, count=None, sources=None, destinations=None) <nano.rpc.Client.republish>`

.. .. py:function:: nano.rpc.Client.republish(hash, count=None, sources=None, destinations=None)

..
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

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.republish(
   ...     hash="991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"
   ... )
   [
       "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
       "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
   ]


successors
----------

Returns a list of block hashes in the account chain ending at **block** up to **count**
:py:func:`nano.rpc.Client.successors(block, count) <nano.rpc.Client.successors>`

.. .. py:function:: nano.rpc.Client.successors(block, count)

..
   Returns a list of block hashes in the account chain ending at
   **block** up to **count**

   :param block: Hash of block to start returning successors for
   :type block: str

   :param count: Max number of successor blocks to return
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.successors(
   ...     block="991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
   ...     count=1
   ... )
   [
       "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
   ]


unchecked
---------

Returns a list of pairs of unchecked synchronizing block hash and its json representation up to **count**
:py:func:`nano.rpc.Client.unchecked(count=None) <nano.rpc.Client.unchecked>`

.. .. py:function:: nano.rpc.Client.unchecked(count=None)

..
   Returns a list of pairs of unchecked synchronizing block hash and its
   json representation up to **count**

   .. version 8.0 required

   :param count: Max amount of unchecked blocks to return
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

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


unchecked_clear
---------------

Clear unchecked synchronizing blocks
:py:func:`nano.rpc.Client.unchecked_clear() <nano.rpc.Client.unchecked_clear>`

.. .. py:function:: nano.rpc.Client.unchecked_clear()

..
   Clear unchecked synchronizing blocks

   .. enable_control required
   .. version 8.0 required

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.unchecked_clear()
   True


unchecked_get
-------------

Retrieves a json representation of unchecked synchronizing block by **hash**
:py:func:`nano.rpc.Client.unchecked_get(hash) <nano.rpc.Client.unchecked_get>`

.. .. py:function:: nano.rpc.Client.unchecked_get(hash)

..
   Retrieves a json representation of unchecked synchronizing block by
   **hash**

   .. version 8.0 required

   :param hash: Hash of unchecked block to get
   :type hash: str

   :raises: :py:exc:`nano.rpc.RPCException`

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


unchecked_keys
--------------

Retrieves unchecked database keys, blocks hashes & a json representations of unchecked pending blocks starting from **key** up to **count**
:py:func:`nano.rpc.Client.unchecked_keys(key=None, count=None) <nano.rpc.Client.unchecked_keys>`

.. .. py:function:: nano.rpc.Client.unchecked_keys(key=None, count=None)

..
   Retrieves unchecked database keys, blocks hashes & a json
   representations of unchecked pending blocks starting from **key** up
   to **count**

   .. version 8.0 required

   :param key: Starting key to return unchecked keys for
   :type key: str

   :param count: Max number of keys/blocks to return
   :type count: int

   :raises: :py:exc:`nano.rpc.RPCException`

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


work_validate
-------------

Check whether **work** is valid for block
:py:func:`nano.rpc.Client.work_validate(work, hash) <nano.rpc.Client.work_validate>`

.. .. py:function:: nano.rpc.Client.work_validate(work, hash)

..
   Check whether **work** is valid for block

   :param work: Work to validate
   :type work: str

   :param hash: Hash of block to validate work for
   :type hash: str

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.work_validate(
   ...     work="2bf29ef00786a6bc",
   ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
   ... )
   True


