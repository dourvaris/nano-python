.. _global-ref:

Global
======

available_supply
----------------

Returns how many rai are in the public supply
:py:func:`nano.rpc.Client.available_supply() <nano.rpc.Client.available_supply>`

.. .. py:function:: nano.rpc.Client.available_supply()

..
   Returns how many rai are in the public supply

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.available_supply()
   10000


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


frontier_count
--------------

Reports the number of accounts in the ledger
:py:func:`nano.rpc.Client.frontier_count() <nano.rpc.Client.frontier_count>`

.. .. py:function:: nano.rpc.Client.frontier_count()

..
   Reports the number of accounts in the ledger

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.frontier_count()
   1000


representatives
---------------

Returns a list of pairs of representative and its voting weight
:py:func:`nano.rpc.Client.representatives(count=None, sorting=False) <nano.rpc.Client.representatives>`

.. .. py:function:: nano.rpc.Client.representatives(count=None, sorting=False)

..
   Returns a list of pairs of representative and its voting weight

   :param count: Max amount of representatives to return
   :type count: int

   :param sorting: If true, sorts by weight
   :type sorting: bool

   :raises: :py:exc:`nano.rpc.RPCException`

   >>> rpc.representatives()
   {
       "xrb_1111111111111111111111111111111111111111111111111117353trpda":
           3822372327060170000000000000000000000,
       "xrb_1111111111111111111111111111111111111111111111111awsq94gtecn":
           30999999999999999999999999000000,
       "xrb_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi":
           0
   }
