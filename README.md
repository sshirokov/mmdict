![CI Status](https://github.com/sshirokov/mmdict/actions/workflows/main.yml/badge.svg)

![imma do it](./images/dict-so-configurable.png)

## What is it

A set of dictionary classes that allow an aliasing of keys to other keys consistently, and a follow up implementation that does the same thing without concern for the case of string keys while preserving case for output and iteration.

Neither implementation assumes string keys, so anything `Hashable` should remain compatible for all keys in the API.

It's still directly comparable (`==`, `in`, `.get()`, etc) and access compatible with `dict()`, and offers a mild framework for implementing key-transforming dictionaries somewhat painlessly with a decent test backing.

## Does it work?

Yes, check this out.

```python
from mmdict import MultiDict

data = {"test": "ok"}
alternatives = {"test": ["also", "as well"]}
d = MultiDict(data, aliases=alternatives)

# True
d["also"] == "ok"

# True
d["as well"] == d["test"]
```

```python
from mmdict import CaselessMultiDict

d = CaselessMultiDict({"Test": "not ok"})

# A super valid write, because we're a regular dict() right?
d["Test"] = "ok"

# Oh wow, `True`, because `"Test"` and `"test"` are caselessly the same
d["test"] == "ok"

# True, because, the case of the initial write is preserved for iteration
list(d.keys()) == ["Test"]
```

## Development Setup

*nix

```bash
python -mvenv .venv
. .venv/bin/activate
```

PowerShell

```powershell
python -mvenv .venv
.\.venv\Scripts\Activate.ps1
```

Then, for both platforms

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip install -e .
```

## Running tests

With the virtual environment activated, use the multi-platform script to run the test suite.

```bash
script/test.sh.ps1
```

It's a very thin thin wrapper around bootstrapping the test run with python.
