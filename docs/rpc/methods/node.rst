.. _node-ref:

Node
====

bootstrap
---------

Initialize bootstrap to specific **IP address** and **port**
:py:func:`nano.rpc.Client.bootstrap(address, port) <nano.rpc.Client.bootstrap>`

.. .. py:function:: nano.rpc.Client.bootstrap(address, port)

..
   Initialize bootstrap to specific **IP address** and **port**

   :param address: Ip address to bootstrap
   :type address: str

   :param port: Port to bootstrap
   :type port: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.bootstrap(address="::ffff:138.201.94.249", port="7075")
   True

bootstrap_any
-------------

Initialize multi-connection bootstrap to random peers
:py:func:`nano.rpc.Client.bootstrap_any() <nano.rpc.Client.bootstrap_any>`

.. .. py:function:: nano.rpc.Client.bootstrap_any()

..
   Initialize multi-connection bootstrap to random peers

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.bootstrap_any()
   True

keepalive
---------

Tells the node to send a keepalive packet to **address**:**port**
:py:func:`nano.rpc.Client.keepalive(address, port) <nano.rpc.Client.keepalive>`

.. .. py:function:: nano.rpc.Client.keepalive(address, port)

..
   Tells the node to send a keepalive packet to **address**:**port**

   .. enable_control required

   :param address: IP address of node to send keepalive packet to
   :type address: str

   :param port: Port of node to send keepalive packet to
   :type port: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.keepalive(address="::ffff:192.168.1.1", port=1024)
   True

peers
-----

Returns a list of pairs of peer IPv6:port and its node network version
:py:func:`nano.rpc.Client.peers() <nano.rpc.Client.peers>`

.. .. py:function:: nano.rpc.Client.peers()

..
   Returns a list of pairs of peer IPv6:port and its node network version

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.peers()
   {
       "[::ffff:172.17.0.1]:32841": 3
   }

receive_minimum
---------------

Returns receive minimum for node
:py:func:`nano.rpc.Client.receive_minimum() <nano.rpc.Client.receive_minimum>`

.. .. py:function:: nano.rpc.Client.receive_minimum()

..
   Returns receive minimum for node

   .. enable_control required
   .. version 8.0 required

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.receive_minimum()
   1000000000000000000000000


receive_minimum_set
-------------------

Set **amount** as new receive minimum for node until restart
:py:func:`nano.rpc.Client.receive_minimum_set(amount) <nano.rpc.Client.receive_minimum_set>`

.. .. py:function:: nano.rpc.Client.receive_minimum_set(amount)

..
   Set **amount** as new receive minimum for node until restart

   .. enable_control required
   .. version 8.0 required

   :param amount: Amount in raw to set as minimum to receive
   :type amount: int

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.receive_minimum_set(amount=1000000000000000000000000000000)
   True

search_pending_all
------------------

Tells the node to look for pending blocks for any account in all available wallets
:py:func:`nano.rpc.Client.search_pending_all() <nano.rpc.Client.search_pending_all>`

.. .. py:function:: nano.rpc.Client.search_pending_all()

..
   Tells the node to look for pending blocks for any account in all
   available wallets

   .. enable_control required
   .. version 8.0 required

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.search_pending_all()
   True


stop
----

Stop the node
:py:func:`nano.rpc.Client.stop() <nano.rpc.Client.stop>`

.. .. py:function:: nano.rpc.Client.stop()

..
   Stop the node

   .. enable_control required

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.stop()
   True


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


version
-------

Returns the node's RPC version
:py:func:`nano.rpc.Client.version() <nano.rpc.Client.version>`

.. .. py:function:: nano.rpc.Client.version()

..
   Returns the node's RPC version

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.version()
   {
       "rpc_version": 1,
       "store_version": 10,
       "node_vendor": "RaiBlocks 9.0"
   }


