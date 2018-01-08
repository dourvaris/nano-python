# RaiBlocks Python RPC client for rai_node

[![Build Status](https://travis-ci.org/dourvaris/raiblocks-py.svg?branch=master)](https://travis-ci.org/dourvaris/raiblocks-py)
[![Coverage](./coverage.svg)](https://travis-ci.org/dourvaris/raiblocks-py)

A python wrapper for the [RaiBlocks RPC server](https://github.com/clemahieu/raiblocks)
which tries to make it a little easier to work with by converting RPC responses
to native python ones and exposing a pythonic api for making RPC calls.

Note: This library is still new so there may be bugs and api changes, PRs are welcome.

## Install

```
pip install raiblocks
```

## Usage

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

```
    # Returns a list
    >>> rpc.pending(
    ...     "xrb_1111111111111111111111111111111111111111111111111117353trpda")
    [
        '3342AEE6ED02A3ED8D84A2EEE4808157C35EB536D464C7EAD66CFFA23232F14C',
        '1AAE335A94C5DA1E4E1D0B45C3B100CCA241CC5BC557E24BB367C779D55E3A0C',
        '20D5D6EA5CA355B11A0E3C11A74FBB4E91D126F4B3FD97232945D451A621E6F7'
    ]
```

```
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


