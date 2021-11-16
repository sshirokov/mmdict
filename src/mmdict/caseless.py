from typing import Any, Hashable, List, Union
from mmdict.multidict import MultiDict

class CaselessMultiDict(MultiDict):
    def __init__(self, *args, **kwargs):
        # A mapping of the {storage key -> supplied key}
        # Keys that are not transformed are not stored.
        self.storage_to_external = {}

        super().__init__(*args, **kwargs)

    # New internal helpers for case insensitivity and external
    # key mapping tracking.
    def __casefold_when_possible(self, key: Union[str, Any]) -> Union[str, Any]:
        '''
        Call `key.upcase()` if key is a string, otherwise
        return the input unchanged.
        '''
        if isinstance(key, str):
            return key.casefold()
        return key

    def __try_to_forget_external_name(self, storage_key):
        '''
        Attemp to forget an external name for a storage key if it no longer has
        a value in the sore, and has no remaining aliases defined.
        Otherwise, do nothing.
        '''
        remaining_aliases = self.storage_to_aliases.get(storage_key, set())
        has_data = storage_key in self.value_store
        if not len(remaining_aliases) and not has_data:
            if storage_key in self.storage_to_aliases:
                del self.storage_to_aliases[storage_key]

    # Key mapping to and from presentation and storage
    def _to_storage_key(self, key):
        return self.__casefold_when_possible(
            super()._to_storage_key(key)
        )

    def _to_internal_alias(self, key):
        return self.__casefold_when_possible(
            super()._to_internal_alias(key)
        )

    def _to_external_key(self, key):
        not_found = KeyError("not found")
        external = self.storage_to_external.get(key, not_found)
        if external != not_found:
            return external
        return super()._to_external_key(key)

    # Protocol methods to keep track of representation and storage keys
    def alias(self, canonical: Hashable, aliases: List[Hashable]):
        storage_key = self._to_storage_key(canonical)
        self.storage_to_external.setdefault(storage_key, canonical)
        return super().alias(canonical, aliases)

    def unalias(self, alias: Hashable) -> bool:
        storage_key = self._to_storage_key(alias)
        result = super().unalias(alias)
        self.__try_to_forget_external_name(storage_key)
        return result

    def __setitem__(self, key, value):
        # We do not need to track the given names of aliases
        if not self.is_alias(key):
            storage_key = self._to_storage_key(key)
            # We only need to track the first given value for a key when:
            #   * It is not already defined as a destination by an alias declaration.
            #   * Only if we transform the key
            #   * We have not used the storage slot before
            has_value = storage_key in self.value_store
            is_destination = storage_key in self.storage_to_aliases
            if not is_destination and not has_value:
                self.storage_to_external[storage_key] = key

        return super().__setitem__(key, value)

    def __delitem__(self, key):
        result = super().__delitem__(key)
        storage_key = self._to_storage_key(key)
        self.__try_to_forget_external_name(storage_key)
        return result
