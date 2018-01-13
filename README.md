# RaiBlocks Python RPC client + various tools

[![Build Status](https://travis-ci.org/dourvaris/raiblocks-py.svg?branch=master)](https://travis-ci.org/dourvaris/raiblocks-py)
[![Coverage](./coverage.svg)](https://travis-ci.org/dourvaris/raiblocks-py)

A python wrapper for the [RaiBlocks RPC server](https://github.com/clemahieu/raiblocks)
which tries to make it a little easier to work with by converting RPC responses
to native python ones and exposing a pythonic api for making RPC calls.

Also included are various utilities such as for converting amounts and named accounts.

Note: This library is still new so there may be bugs and api changes, PRs are welcome.

## Install

```
pip install raiblocks
```

## Usage


### RPC Client

```python
    >>> from raiblocks import RPCClient
    >>> rpc = RPCClient('http://localhost:7076')
    >>> rpc.version()
    {'rpc_version': 1, 'store_version': 10, 'node_vendor': 'RaiBlocks 9.0'}
    >>> rpc.peers()
    {
        '[::ffff:75.171.168.5]:7075': 4,
        '[::ffff:108.44.38.183]:1032': 4
    }
```

The client exposes the methods that can be found here: https://github.com/clemahieu/raiblocks/wiki/RPC-protocol

At the moment the client replicates the RPC API which means there are some
instances where the same method will return different types eg:

```python
    # Returns a list
    >>> rpc.pending(
    ...     "xrb_1111111111111111111111111111111111111111111111111117353trpda")
    [
        '3342AEE6ED02A3ED8D84A2EEE4808157C35EB536D464C7EAD66CFFA23232F14C',
        '1AAE335A94C5DA1E4E1D0B45C3B100CCA241CC5BC557E24BB367C779D55E3A0C',
        '20D5D6EA5CA355B11A0E3C11A74FBB4E91D126F4B3FD97232945D451A621E6F7'
    ]
```

```python
    # Returns a dict
    >>> rpc.pending(
    ...     "xrb_1111111111111111111111111111111111111111111111111117353trpda",
    ...     threshold=10e30)
    {
        '3342AEE6ED02A3ED8D84A2EEE4808157C35EB536D464C7EAD66CFFA23232F14C': 100000000000000000000000000000000,
        '1AAE335A94C5DA1E4E1D0B45C3B100CCA241CC5BC557E24BB367C779D55E3A0C': 95000000000000000000000000000000,
        '20D5D6EA5CA355B11A0E3C11A74FBB4E91D126F4B3FD97232945D451A621E6F7': 36968007000000000000000000000000
    }
```

### Conversion tools

There are functions for all conversions such as `raw_to_krai`, `XRB_to_raw` etc. as well as a general case `converter` function:

```python
>>> from raiblocks import UNITS_TO_RAW, converter, XRB_to_raw, raw_to_XRB
>>> converter(12, from_unit='XRB', to_unit='raw')
Decimal('1.2E+31')
>>> XRB_to_raw(12)
Decimal('1.2E+31')
>>> raw_to_XRB(25000000000000000000000000)
Decimal('0.000025')
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
```

### Known Accounts / Constants

```python
>>> from raiblocks import GENESIS_BLOCK, GENESIS_AMOUNT, KNOWN_ACCOUNT_IDS, KNOWN_ACCOUNT_NAMES
>>> KNOWN_ACCOUNT_IDS['xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est']
'Developer Fund'
>>> KNOWN_ACCOUNT_NAMES['Burn']
'xrb_1111111111111111111111111111111111111111111111111111hifc8npp'
>>> GENESIS_BLOCK
'991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948'
>>> GENESIS_AMOUNT
340282366920938463463374607431768211455
```

## Development
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt -r test-requirements.txt
```

### Tests

Regular
```
pytest
```

Coverage:
```
./coverage
```


