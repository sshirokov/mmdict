from mmdict.multidict import MultiDict

class CaselessMultiDict(MultiDict):
    def __casefold_when_possible(self, key):
        if isinstance(key, str):
            return key.casefold()
        return key

    def _to_storage_key(self, key):
        return self.__casefold_when_possible(
            super()._to_storage_key(key)
        )

    def _to_internal_alias(self, key):
        return self.__casefold_when_possible(
            super()._to_internal_alias(key)
        )

    def _to_external_key(self, key):
        return super()._to_external_key(key)
