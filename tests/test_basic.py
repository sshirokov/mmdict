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

    def test__can_tell_if_key_does_not_exist(self):
        d = mmdict.MultiDict({"test": "ok"})
        self.assertFalse("not present" in d)

    def test__can_list_all_keys(self):
        initial = {"test": "ok", "two": 2}
        d = mmdict.MultiDict(initial)
        self.assertCountEqual(d.keys(), initial.keys())

    def test__can_delete_a_key(self):
        initial = {"test": "ok", "remaining": 2}
        d = mmdict.MultiDict(initial)
        del d["test"]
        self.assertCountEqual(d.keys(), ["remaining"])

    def test__will_fail_to_delete_unknown_key(self):
        initial = {"test": "ok"}
        d = mmdict.MultiDict(initial)
        with self.assertRaises(KeyError):
            del d["not present"]


if __name__ == '__main__':
    unittest.main()
