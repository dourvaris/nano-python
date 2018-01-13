.. _global-ref:

Global
======

available_supply
----------------

Returns how many rai are in the public supply 
:py:func:`raiblocks.rpc.RPCClient.available_supply() <raiblocks.rpc.RPCClient.available_supply>`

.. .. py:function:: raiblocks.rpc.RPCClient.available_supply()

..    
   Returns how many rai are in the public supply
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.available_supply()
   10000
   

block_count
-----------

Reports the number of blocks in the ledger and unchecked synchronizing blocks 
:py:func:`raiblocks.rpc.RPCClient.block_count() <raiblocks.rpc.RPCClient.block_count>`

.. .. py:function:: raiblocks.rpc.RPCClient.block_count()

..    
   Reports the number of blocks in the ledger and unchecked synchronizing
   blocks
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.block_count()
   {
     "count": 1000,
     "unchecked": 10
   }
   

block_count_type
----------------

Reports the number of blocks in the ledger by type (send, receive, open, change) 
:py:func:`raiblocks.rpc.RPCClient.block_count_type() <raiblocks.rpc.RPCClient.block_count_type>`

.. .. py:function:: raiblocks.rpc.RPCClient.block_count_type()

..    
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
   

frontier_count
--------------

Reports the number of accounts in the ledger 
:py:func:`raiblocks.rpc.RPCClient.frontier_count() <raiblocks.rpc.RPCClient.frontier_count>`

.. .. py:function:: raiblocks.rpc.RPCClient.frontier_count()

..    
   Reports the number of accounts in the ledger
   
   :raises: :py:exc:`raiblocks.rpc.RPCException`
   
   >>> rpc.frontier_count()
   1000
   

representatives
---------------

Returns a list of pairs of representative and its voting weight 
:py:func:`raiblocks.rpc.RPCClient.representatives(count=None, sorting=False) <raiblocks.rpc.RPCClient.representatives>`

.. .. py:function:: raiblocks.rpc.RPCClient.representatives(count=None, sorting=False)

..    
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
   
   

