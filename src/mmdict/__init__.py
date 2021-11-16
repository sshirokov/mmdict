from collections.abc import MutableMapping
from typing import List, Hashable

class AliasExistsError(KeyError): pass

class MultiDict(MutableMapping):
    def __init__(self, initial={}, aliases={}):
        # Actual storage of values, by cannonical key
        self.value_store = {}
        # Mapping of alias -> cannonical key
        self.alias_to_storage = {}

        # Load any constructor supplied aliases to prepare for
        # any constructor-supplied data
        for real, alias in aliases.items():
            if not isinstance(alias, List):
                alias = [alias]
            self.alias(real, alias)

        # Load any constructor-supplied data. We simply let the
        # `MutableMapping` protocol take the wheel from here
        self.update(initial)

    def alias(self, canonical: Hashable, aliases: List[Hashable]):
        not_found = KeyError("Not Found")
        for alias in aliases:
            # We are not alowed to overwrite an alias with an alias to a different key.
            #
            # This prevents an initialization such as as
            #   `MultiDict(..., aliases={"one": ["One", 1], "two": ["One", "Two"]})`
            # from silently replacing, or abitrarily chosing to keep, one definition of
            #   `"One" -> "one"` or `"One" -> "two"`
            #
            # We use a sentinel `not_found` to avoid failing on falsey but valid keys.
            existing = self.alias_to_storage.get(alias, not_found)
            if existing not in (canonical, not_found):
                raise AliasExistsError(f'{alias} is already defined as an alias for {canonical}')
            self.alias_to_storage[alias] = canonical

    def unalias(self, alias: Hashable) -> bool:
        '''
        Remove an alias to a canonical key. Returns `True` if the alias was removed
        `False` if no action was taken.
        '''
        if alias not in self.alias_to_storage:
            return False
        del self.alias_to_storage[alias]
        return True

    def _to_cannonical_key(self, key):
        '''
        Transform a supplied key into the key used to store values in
        `self.value_store` by resolving aliases.
        '''
        return self.alias_to_storage.get(key, key)

    def _to_external_key(self, key):
        '''
        Transforms a `self.value_store` key into an externally presentable key.
        '''
        return key

    # MutableMapping protocol definitions
    def __getitem__(self, key):
        value_store_key = self._to_cannonical_key(key)
        try:
            return self.value_store[value_store_key]
        except KeyError:
            # Re-raise the `KeyError` with the passed in key instead
            # of the transformed, canonical storage one.
            raise KeyError(key)

    def __setitem__(self, key, value):
        value_store_key = self._to_cannonical_key(key)
        self.value_store[value_store_key] = value

    def __delitem__(self, key):
        value_store_key = self._to_cannonical_key(key)
        del self.value_store[key]

    def __iter__(self):
        return (self._to_external_key(k) for k in self.value_store.keys())

    def __len__(self):
        return len(self.value_store)
