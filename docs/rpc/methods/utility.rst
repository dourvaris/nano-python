.. _utility-ref:

Utility
=======

deterministic_key
-----------------

Derive deterministic keypair from **seed** based on **index** 
:py:func:`raiblocks.rpc.RPCClient.deterministic_key(seed, index) <raiblocks.rpc.RPCClient.deterministic_key>`

.. .. py:function:: raiblocks.rpc.RPCClient.deterministic_key(seed, index)

..    
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
   

key_create
----------

Generates an **adhoc random keypair** 
:py:func:`raiblocks.rpc.RPCClient.key_create() <raiblocks.rpc.RPCClient.key_create>`

.. .. py:function:: raiblocks.rpc.RPCClient.key_create()

..    
   Generates an **adhoc random keypair**
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.key_create()
   {
     "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
     "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
     "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
   }
   

key_expand
----------

Derive public key and account number from **private key** 
:py:func:`raiblocks.rpc.RPCClient.key_expand(key) <raiblocks.rpc.RPCClient.key_expand>`

.. .. py:function:: raiblocks.rpc.RPCClient.key_expand(key)

..    
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
   

krai_from_raw
-------------

Divide a raw amount down by the krai ratio. 
:py:func:`raiblocks.rpc.RPCClient.krai_from_raw(amount) <raiblocks.rpc.RPCClient.krai_from_raw>`

.. .. py:function:: raiblocks.rpc.RPCClient.krai_from_raw(amount)

..    
   Divide a raw amount down by the krai ratio.
   
   :param amount: Amount in raw to convert to krai
   :type amount: int
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.krai_from_raw(amount=1000000000000000000000000000)
   1

krai_to_raw
-----------

Multiply an krai amount by the krai ratio. 
:py:func:`raiblocks.rpc.RPCClient.krai_to_raw(amount) <raiblocks.rpc.RPCClient.krai_to_raw>`

.. .. py:function:: raiblocks.rpc.RPCClient.krai_to_raw(amount)

..    
   Multiply an krai amount by the krai ratio.
   
   :param amount: Amount in krai to convert to raw
   :type amount: int
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.krai_to_raw(amount=1)
   1000000000000000000000000000
   

mrai_from_raw
-------------

Divide a raw amount down by the Mrai ratio. 
:py:func:`raiblocks.rpc.RPCClient.mrai_from_raw(amount) <raiblocks.rpc.RPCClient.mrai_from_raw>`

.. .. py:function:: raiblocks.rpc.RPCClient.mrai_from_raw(amount)

..    
   Divide a raw amount down by the Mrai ratio.
   
   :param amount: Amount in raw to convert to Mrai
   :type amount: int
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.mrai_from_raw(amount=1000000000000000000000000000000)
   1
   

mrai_to_raw
-----------

Multiply an Mrai amount by the Mrai ratio. 
:py:func:`raiblocks.rpc.RPCClient.mrai_to_raw(amount) <raiblocks.rpc.RPCClient.mrai_to_raw>`

.. .. py:function:: raiblocks.rpc.RPCClient.mrai_to_raw(amount)

..    
   Multiply an Mrai amount by the Mrai ratio.
   
   :param amount: Amount in Mrai to convert to raw
   :type amount: int
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.mrai_to_raw(amount=1)
   1000000000000000000000000000000
   

rai_from_raw
------------

Divide a raw amount down by the rai ratio. 
:py:func:`raiblocks.rpc.RPCClient.rai_from_raw(amount) <raiblocks.rpc.RPCClient.rai_from_raw>`

.. .. py:function:: raiblocks.rpc.RPCClient.rai_from_raw(amount)

..    
   Divide a raw amount down by the rai ratio.
   
   :param amount: Amount in raw to convert to rai
   :type amount: int
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.rai_from_raw(amount=1000000000000000000000000)
   1
   

rai_to_raw
----------

Multiply an rai amount by the rai ratio. 
:py:func:`raiblocks.rpc.RPCClient.rai_to_raw(amount) <raiblocks.rpc.RPCClient.rai_to_raw>`

.. .. py:function:: raiblocks.rpc.RPCClient.rai_to_raw(amount)

..    
   Multiply an rai amount by the rai ratio.
   
   :param amount: Amount in rai to convert to raw
   :type amount: int
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.rai_to_raw(amount=1)
   1000000000000000000000000
   

