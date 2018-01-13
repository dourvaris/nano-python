.. _utilities-ref:

Utilities
==========


Conversion tools
----------------

For converting between rai/xrb amounts.

The :meth:`raiblocks.conversion.convert` function takes ``int``, ``Decimal`` or ``string`` arguments (no ``float``):

.. code-block:: python

    >>> from raiblocks import convert
    >>> convert(12, from_unit='XRB', to_unit='raw')
    Decimal('1.2E+31')

    >>> converter(0.4, from_unit='krai', to_unit='XRB')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: float values can lead to unexpected
    precision loss, please use a Decimal or string
    eg. converter('0.4', 'krai', 'XRB')

    >>> convert('0.4', from_unit='krai', to_unit='XRB')
    Decimal('0.0004')



.. WARNING::
   Careful not to mix up ``'XRB'`` and ``'xrb'`` as they are different units

    >>> convert(2000000000000000000000000, 'raw', 'XRB')
    Decimal('0.000002')
    >>> convert(2000000000000000000000000, 'raw', 'xrb')
    Decimal('2')

For a dict of all available units and their amount in raw:

    >>> from raiblocks import UNITS_TO_RAW
    >>> UNITS_TO_RAW
    {'Grai': Decimal('1000000000000000000000000000000000'),
     'Gxrb': Decimal('1000000000000000000000000000000000'),
     'Mrai': Decimal('1000000000000000000000000000000'),
     'Mxrb': Decimal('1000000000000000000000000000000'),
     'XRB': Decimal('1000000000000000000000000000000'),
     'krai': Decimal('1000000000000000000000000000'),
     'kxrb': Decimal('1000000000000000000000000000'),
     'mrai': Decimal('1000000000000000000000'),
     'mxrb': Decimal('1000000000000000000000'),
     'rai': Decimal('1000000000000000000000000'),
     'raw': 1,
     'urai': Decimal('1000000000000000000'),
     'uxrb': Decimal('1000000000000000000'),
     'xrb': Decimal('1000000000000000000000000')}

Known Accounts / Constants
--------------------------

.. code-block:: python

    >>> from raiblocks import GENESIS_BLOCK_HASH, KNOWN_ACCOUNT_IDS, KNOWN_ACCOUNT_NAMES
    >>> KNOWN_ACCOUNT_IDS['xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est']
    'Developer Fund'
    >>> KNOWN_ACCOUNT_NAMES['Burn']
    'xrb_1111111111111111111111111111111111111111111111111111hifc8npp'
    >>> GENESIS_BLOCK_HASH
    '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948'
