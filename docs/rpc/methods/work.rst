.. _work-ref:

Work
====

wallet_work_get
---------------

Returns a list of pairs of account and work from **wallet** 
:py:func:`raiblocks.rpc.RPCClient.wallet_work_get(wallet) <raiblocks.rpc.RPCClient.wallet_work_get>`

.. .. py:function:: raiblocks.rpc.RPCClient.wallet_work_get(wallet)

..    
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
   

work_cancel
-----------

Stop generating **work** for block 
:py:func:`raiblocks.rpc.RPCClient.work_cancel(hash) <raiblocks.rpc.RPCClient.work_cancel>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_cancel(hash)

..    
   Stop generating **work** for block
   
   .. enable_control required
   
   :param hash: Hash to stop generating work for
   :type hash: str
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.work_cancel(
   ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
   ... )
   True
   

work_generate
-------------

Generates **work** for block 
:py:func:`raiblocks.rpc.RPCClient.work_generate(hash) <raiblocks.rpc.RPCClient.work_generate>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_generate(hash)

..    
   Generates **work** for block
   
   .. enable_control required
   
   :param hash: Hash to start generating **work** for
   :type hash: str
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.work_generate(
   ...     hash="718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
   ... )
   "2bf29ef00786a6bc"
   

work_get
--------

Retrieves work for **account** in **wallet** 
:py:func:`raiblocks.rpc.RPCClient.work_get(wallet, account) <raiblocks.rpc.RPCClient.work_get>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_get(wallet, account)

..    
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
   

work_peer_add
-------------

Add specific **IP address** and **port** as work peer for node until restart 
:py:func:`raiblocks.rpc.RPCClient.work_peer_add(address, port) <raiblocks.rpc.RPCClient.work_peer_add>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_peer_add(address, port)

..    
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
   

work_peers
----------

Retrieve work peers 
:py:func:`raiblocks.rpc.RPCClient.work_peers() <raiblocks.rpc.RPCClient.work_peers>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_peers()

..    
   Retrieve work peers
   
   .. enable_control required
   .. version 8.0 required
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.work_peers()
   [
       "::ffff:172.17.0.1:7076"
   ]
   

work_peers_clear
----------------

Clear work peers node list until restart 
:py:func:`raiblocks.rpc.RPCClient.work_peers_clear() <raiblocks.rpc.RPCClient.work_peers_clear>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_peers_clear()

..    
   Clear work peers node list until restart
   
   .. enable_control required
   .. version 8.0 required
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.work_peers_clear()
   True
   

work_set
--------

Set **work** for **account** in **wallet** 
:py:func:`raiblocks.rpc.RPCClient.work_set(wallet, account, work) <raiblocks.rpc.RPCClient.work_set>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_set(wallet, account, work)

..    
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

work_validate
-------------

Check whether **work** is valid for block 
:py:func:`raiblocks.rpc.RPCClient.work_validate(work, hash) <raiblocks.rpc.RPCClient.work_validate>`

.. .. py:function:: raiblocks.rpc.RPCClient.work_validate(work, hash)

..    
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
   

