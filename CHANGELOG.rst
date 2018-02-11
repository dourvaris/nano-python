Changelog
=========


Version 2.0.0 (2018-02-11)
--------------------------

- Nano rebrand - the `raiblocks` module has been replaced with `nano`
- Pypi package name is now `nano-python`
- Use `import nano` instead of `import raiblocks`
- rpc client has been renamed from `nano.rpc.RPCClient` to `nano.rpc.Client`


Version 1.1.0 (2018-02-11)
--------------------------

- RPC no longer automatically retries backend calls since this could lead to
  double sends when a `send` call was issued twice due to a timeout
- RPC `.delegators()` now returns voting weights as integers instead of strings
