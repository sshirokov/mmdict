## What is it

A dictionary that allows you to alias keys to a canonical key. Also a case-insentive version, probably.

## Does it work?

Not if this section exists, but also here's a plan

  * [ ] Helper to return a regular dict with canonical keys
  * [ ] `__str__` pretty printer
  * [ ] Helper to return aliases
  * [ ] `mmdict.CaselessMultiDict` - which ignores case on read and write, but preserves it on output

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
