from collections.abc import MutableMapping
from typing import List, Hashable

from mmdict.errors import AliasExistsError

class MultiDict(MutableMapping):
    def __init__(self, initial={}, aliases={}):
        # Actual storage of values, by cannonical key
        self.value_store = {}
        # Mapping of alias -> cannonical key
        self.alias_to_storage = {}
        # Mapping of {cannonical key -> Set[alias: Hashable]}
        self.storage_to_aliases = {}

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
        # We do not want to allow an alias to shadow a destination
        if self.is_alias(canonical):
            raise AliasExistsError(f'Destination {canonical} is already defined as an alias.')

        # Ensure that any potential subclass transforms take place
        canonical = self._to_storage_key(canonical)
        not_found = KeyError("Not Found")

        for alias in aliases:
            alias_key = self._to_internal_alias(alias)
            # Don't bother aliasing identity
            if canonical == alias_key:
                continue
            # We are not alowed to overwrite an alias with an alias to a different key.
            #
            # This prevents an initialization such as as
            #   `MultiDict(..., aliases={"one": ["One", 1], "two": ["One", "Two"]})`
            # from silently replacing, or abitrarily chosing to keep, one definition of
            #   `"One" -> "one"` or `"One" -> "two"`
            #
            # We use a sentinel `not_found` to avoid failing on falsey but valid keys.
            existing = self.alias_to_storage.get(alias_key, not_found)
            if existing not in (canonical, not_found):
                existing_external = self._to_external_key(existing)
                raise AliasExistsError(f'{alias} is already defined as an alias for {existing_external}')

            # Store forward and backward refferences for the alias
            self.alias_to_storage[alias_key] = canonical
            aliases_for_cannonical = self.storage_to_aliases.setdefault(canonical, set())
            aliases_for_cannonical.add(alias_key)

    def unalias(self, alias: Hashable) -> bool:
        '''
        Remove an alias to a canonical key.

        Returns `True` if the alias was removed `False` if no action was taken.
        '''
        not_found = KeyError("not found")
        alias_key = self._to_internal_alias(alias)
        storage_key = self.alias_to_storage.get(alias_key, not_found)
        if storage_key == not_found:
            return False

        del self.alias_to_storage[alias_key]
        self.storage_to_aliases[storage_key].remove(alias_key)
        return True

    def unalias_all(self, key: Hashable):
        '''
        Remove any aliases associated with `key`, first by following
        the aliases to the cannoncal key, then clearing all aliases for
        that cannonical key.
        '''
        storage_key = self._to_storage_key(key)
        aliases = self.storage_to_aliases.get(storage_key, set())
        for alias in aliases.copy():
            self.unalias(alias)

    def is_alias(self, key: Hashable) -> bool:
        return self._to_internal_alias(key) in self.alias_to_storage

    def _to_internal_alias(self, key):
        '''
        Transforms a supplied alias to an internal alias.

        Not used in the base, but allows for easier normalization
        of aliases.
        '''
        return key

    def _to_storage_key(self, key):
        '''
        Transform a supplied key into the key used to store values in
        `self.value_store` by resolving aliases.
        '''
        internal_alias = self._to_internal_alias(key)
        return self.alias_to_storage.get(internal_alias, key)

    def _to_external_key(self, key):
        '''
        Transforms a `self.value_store` key into an externally presentable key.

        Not actively used here, but tied into `__iter__`, so that subclasses can
        differentiate between the storage key and the user supplied key that
        produced it.

        For example, using downcased storage keys, but preserving case for iteration.
        '''
        return key

    # MutableMapping protocol definitions
    def __getitem__(self, key):
        value_store_key = self._to_storage_key(key)
        try:
            return self.value_store[value_store_key]
        except KeyError:
            # Re-raise the `KeyError` with the passed in key instead
            # of the transformed, canonical storage one.
            raise KeyError(key)

    def __setitem__(self, key, value):
        value_store_key = self._to_storage_key(key)
        self.value_store[value_store_key] = value

    def __delitem__(self, key):
        value_store_key = self._to_storage_key(key)
        del self.value_store[value_store_key]

    def __iter__(self):
        return (self._to_external_key(k) for k in self.value_store.keys())

    def __len__(self):
        return len(self.value_store)

    # Pretty-printers and exports
    def to_dict(self) -> dict:
        '''
        Return a regular `dict` of the canonical keys and values
        '''
        return dict(self.items())

    def __repr__(self):
        class_name = self.__class__.__name__
        data = self.to_dict()
        aliases = self.storage_to_aliases
        return f'<{class_name}: {data} aliases={aliases}>'
