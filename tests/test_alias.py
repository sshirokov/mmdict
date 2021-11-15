import unittest

import mmdict

class MultiDictAliasTests(unittest.TestCase):
    def test__declare_and_read_through_single_alias(self):
        data = {"test": "ok"}
        d = mmdict.MultiDict(data)
        d.alias("test", ["also"])
        self.assertEqual(d["also"], "ok")

    def test__declare_and_read_through_multiple_aliases(self):
        data = {"test": "ok"}
        d = mmdict.MultiDict(data)
        d.alias("test", ["also", "as well"])

        self.assertEqual(d["also"], "ok")
        self.assertEqual(d["as well"], "ok")

    def test__declare_and_read_through_multiple_aliases_using_constructor(self):
        data = {"test": "ok"}
        aliases = {"test": ["also", "as well"]}
        d = mmdict.MultiDict(data, aliases)

        self.assertEqual(d["also"], "ok")
        self.assertEqual(d["as well"], "ok")

    def test__declare_and_read_through_single_alias_using_constructor(self):
        data = {"test": "ok"}
        aliases = {"test": "also"}
        d = mmdict.MultiDict(data, aliases)

        self.assertEqual(d["also"], "ok")




if __name__ == '__main__':
    unittest.main()
