# RaiBlocks Python RPC client for rai_node

[![Build Status](https://travis-ci.org/dourvaris/raiblocks-py.svg?branch=master)](https://travis-ci.org/dourvaris/raiblocks-py)

## Install

```
pip install raiblocks
```

## Development
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt -r test-requirements.txt
```

### Tests

With coverage:
```
py.test --cov-report term:missing --cov=raiblocks
```
