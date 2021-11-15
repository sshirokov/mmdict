## What is it

A dictionary that allows you to alias keys to a canonical key. Also a case-insentive version, probably.

## Does it work?

Not if this section exists, but also here's a plan

  * [ ] `mmdict.MultiDict`
    * [ ] Set aliases on construction
    * [ ] Set aliases after creation
    * [ ] Getting by alias works
    * [ ] Iteration keeps "canonical" key
  * [ ] `mmdict.CaselessMultiDict`
  * [ ] Tests of any kind

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
