========================
RaiBlocks Python Library
========================

.. image:: https://img.shields.io/pypi/l/raiblocks.svg
    :target: https://github.com/dourvaris/raiblocks-python/blob/master/LICENSE

.. image:: https://travis-ci.org/dourvaris/raiblocks-python.svg?branch=1.0.0rc1
    :target: https://travis-ci.org/dourvaris/raiblocks-python

.. image:: https://readthedocs.org/projects/raiblocks-python/badge/?version=latest
    :target: http://raiblocks-python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/dourvaris/raiblocks-python/raw/master/coverage.svg?sanitize=true
    :target: https://travis-ci.org/dourvaris/raiblocks-python

.. image:: https://img.shields.io/pypi/pyversions/raiblocks.svg?style=flat-square
    :target: https://pypi.python.org/pypi/raiblocks

.. image:: https://img.shields.io/pypi/v/raiblocks.svg
    :target: https://pypi.python.org/pypi/raiblocks

This library contains a python wrapper for the RaiBlocks RPC server
which tries to make it a little easier to work with by converting RPC responses
to native python ones and exposing a pythonic api for making RPC calls.

Also included are utilities such as converting rai/xrb and interesting accounts


Installation
============

.. code-block:: text

    pip install raiblocks

Documentation
=============

https://raiblocks-python.readthedocs.io/

RPC client
==========

You can browse the available
`RPC methods list <https://raiblocks-python.readthedocs.io/en/latest/rpc/index.html>`_
or check the
`RPC Client API documentation <https://raiblocks-python.readthedocs.io/en/latest/raiblocks.html#module-raiblocks.rpc>`_
for examples of usage.

.. code-block:: python

    >>> from raiblocks import RPCClient
    >>> rpc = RPCClient('http://localhost:7076')
    >>> rpc.version()
    {
        'rpc_version': 1,
        'store_version': 10,
        'node_vendor': 'RaiBlocks 9.0'
    }
    >>> rpc.peers()
    {
        '[::ffff:75.171.168.5]:7075': 4,
        '[::ffff:108.44.38.183]:1032': 4
    }

Conversion
==========

.. code-block:: python

    >>> from raiblocks import convert
    >>> convert(12, from_unit='XRB', to_unit='raw')
    Decimal('1.2E+31')

    >>> convert(0.4, from_unit='krai', to_unit='XRB')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: float values can lead to unexpected
    precision loss, please use a Decimal or string
    eg. convert('0.4', 'krai', 'XRB')

    >>> convert('0.4', from_unit='krai', to_unit='XRB')
    Decimal('0.0004')


Known Accounts / Constants
==========================

.. code-block:: python

    >>> from raiblocks import GENESIS_BLOCK_HASH
    >>> GENESIS_BLOCK_HASH
    '991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948'


.. code-block:: python

    >>> from raiblocks import KNOWN_ACCOUNT_IDS
    >>> KNOWN_ACCOUNT_IDS['xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est']
    'Developer Fund'


.. code-block:: python

    >>> from raiblocks import KNOWN_ACCOUNT_NAMES
    >>> KNOWN_ACCOUNT_NAMES['Burn']
    'xrb_1111111111111111111111111111111111111111111111111111hifc8npp'


Development
==========

Setup
-----

.. code-block:: text

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.pip -r test-requirements.pip
    python setup.py develop

Running tests
-------------

.. code-block:: text

    # regular
    pytest

    # coverage
    ./coverage


Building docs
-------------

.. code-block:: text

    cd docs

    # generate once
    make html

    # live building
    make live
