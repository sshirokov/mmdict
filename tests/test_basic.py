import unittest

import mmdict

class MultiDictBasicTests(unittest.TestCase):
    def test__can_instantiate_empty(self):
        d = mmdict.MultiDict()
        self.assertIsNotNone(d)

    def test__can_instantiate_with_data(self):
        d = mmdict.MultiDict({"test": "ok"})
        self.assertIsNotNone(d)

    def test__can_read_by_same_key(self):
        d = mmdict.MultiDict()
        d["test"] = "ok"
        self.assertEqual(d["test"], "ok")

    def test__can_insert_into_empty(self):
        d = mmdict.MultiDict()
        d["test"] = "ok"

    def test__can_tell_if_key_exists(self):
        d = mmdict.MultiDict({"test": "ok"})
        self.assertTrue("test" in d)
