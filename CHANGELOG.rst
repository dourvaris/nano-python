Changelog
=========



Version 1.1.0 (2018-01-24)
--------------------------

- RPC no longer automatically retries backend calls since this could lead to
  double sends when a `send` call was issued twice due to a timeout
- RPC `.delegators()` now returns voting weights as integers instead of strings
