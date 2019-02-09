.. _utilities-ref:

Utilities
==========


Conversion tools
----------------

For converting between nano/xrb/rai amounts.

The :meth:`nano.conversion.convert` function takes ``int``, ``Decimal`` or ``string`` arguments (no ``float``):

.. code-block:: python

    >>> from nano import convert
    >>> convert(12, from_unit='NANO', to_unit='raw')
    Decimal('1.2E+31')

    >>> convert(0.4, from_unit='knano', to_unit='NANO')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: float values can lead to unexpected
    precision loss, please use a Decimal or string
    eg. convert('0.4', 'knano', 'NANO')

    >>> convert('0.4', from_unit='knano', to_unit='NANO')
    Decimal('0.0004')



.. WARNING::
   Careful not to mix up ``'NANO'`` and ``'nano'`` as they are different units

    >>> convert(2000000000000000000000000, 'raw', 'NANO')
    Decimal('0.000002')
    >>> convert(2000000000000000000000000, 'raw', 'nano')
    Decimal('2')

For a dict of all available units and their amount in raw:

    >>> from nano import UNITS_TO_RAW
    >>> UNITS_TO_RAW
    {'Gnano': Decimal('1000000000000000000000000000000000'),
     'Grai': Decimal('1000000000000000000000000000000000'),
     'Gxrb': Decimal('1000000000000000000000000000000000'),
     'Mnano': Decimal('1000000000000000000000000000000'),
     'Mrai': Decimal('1000000000000000000000000000000'),
     'Mxrb': Decimal('1000000000000000000000000000000'),
     'NANO': Decimal('1000000000000000000000000000000'),
     'XRB': Decimal('1000000000000000000000000000000'),
     'knano': Decimal('1000000000000000000000000000'),
     'krai': Decimal('1000000000000000000000000000'),
     'kxrb': Decimal('1000000000000000000000000000'),
     'mnano': Decimal('1000000000000000000000'),
     'mrai': Decimal('1000000000000000000000'),
     'mxrb': Decimal('1000000000000000000000'),
     'nano': Decimal('1000000000000000000000000'),
     'rai': Decimal('1000000000000000000000000'),
     'raw': Decimal('1'),
     'unano': Decimal('1000000000000000000'),
     'urai': Decimal('1000000000000000000'),
     'uxrb': Decimal('1000000000000000000'),
     'xrb': Decimal('1000000000000000000000000')}

Known Accounts / Constants
--------------------------

.. code-block:: python

    >>> from nano import GENESIS_BLOCK_HASH, KNOWN_ACCOUNT_IDS, KNOWN_ACCOUNT_NAMES
    >>> KNOWN_ACCOUNT_IDS['xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est']
    'Developer Fund'
    >>> KNOWN_ACCOUNT_NAMES['Burn']
    'xrb_1111111111111111111111111111111111111111111111111111hifc8npp'
    >>> GENESIS_BLOCK_HASH
    '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948'
