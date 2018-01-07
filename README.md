# RaiBlocks Python RPC client for rai_node


## Install

```
pip install raiblocks
```

## Development
```
virtualenv venv
. venv/bin/activate
python setup.py develop
```

### Tests

Normal:
```
py.test
```

Coverage:
```
py.test --cov-report term:missing --cov=raiblocks
```
