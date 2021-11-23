## What is it

A dictionary that allows you to alias keys to a canonical key. Also a case-insentive version, probably.

## Does it work?

Yes

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
