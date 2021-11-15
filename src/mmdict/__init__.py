from collections.abc import MutableMapping

class MultiDict(MutableMapping):
    def __init__(self, initial={}):
        self.value_store = dict()

        for k,v in initial.items():
            self[k] = v

    def _to_cannonical_key(self, key):
        '''
        Transform a supplied key into the key used to store values in
        `self.value_store` by resolving aliases.
        '''
        return key

    # MutableMapping protocol definitions
    def __getitem__(self, key):
        value_store_key = self._to_cannonical_key(key)
        # TODO(sshirokov): Improve the failure error to not just reply with the `value_store_key` - but the passed in key
        #                  and possibly a list of aliases it can be known by
        return self.value_store[value_store_key]

    def __setitem__(self, key, value):
        value_store_key = self._to_cannonical_key(key)
        self.value_store[value_store_key] = value

    def __delitem__(self, key):
        raise NotImplementedError(f"TODO(sshirokov) delete {key}")

    def __iter__(self):
        raise NotImplementedError(f"TODO(sshirokov) return generator of all keys")

    def __len__(self):
        raise NotImplementedError(f"TODO(sshirokov) return number of keys")
