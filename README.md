## What is it

A dictionary that allows you to alias keys to a canonical key. Also a case-insentive version, probably.

## Does it work?

Not if this section exists, but also here's a plan

  * [ ] Helper to return a regular dict with canonical keys
  * [ ] `__str__` pretty printer
  * [ ] Helper to return aliases
  * [ ] `mmdict.CaselessMultiDict` - which ignores case on read and write, but preserves it on output

## Development Setups

*nix

```bash
python -mvenv .venv
. .venv/bin/activate
pip install -e .
```

PowerShell

```powershell
python -mvenv .venv
.\.venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip install -e .
```

## Running tests

```bash
python -m unittest discover -s tests
```
