import unittest

import mmdict

class CaselessMultiDictTests(unittest.TestCase):
    def test__can_read_case_insensitive_keys(self):
        d = mmdict.CaselessMultiDict({"test": "ok"})
        self.assertEqual(d["Test"], "ok")

    def test__can_write_through_case_insensitive_keys(self):
        d = mmdict.CaselessMultiDict({"test": "not ok"})
        d["Test"] = "ok"
        self.assertEqual(d["test"], "ok")

    def test__write_through_case_insensitive_keys_does_not_increase_length(self):
        d = mmdict.CaselessMultiDict({"test": "not ok"})
        len_before = len(d)
        self.assertGreater(len_before, 0)

        d["Test"] = "ok"
        self.assertEqual(len(d), len_before)

    def test__first_unaliased_write_decides_presented_key(self):
        d = mmdict.CaselessMultiDict()
        d["Test"] = "ok"
        self.assertCountEqual(d.keys(), ["Test"])

    def test__unaliased_external_key_does_not_survive_delete(self):
        d = mmdict.CaselessMultiDict()
        d["Test"] = "ok"
        del d["Test"]
        d["tesT"] = "ok"
        self.assertCountEqual(d.keys(), ["tesT"])

    def test__alias_definitions_define_external_key_name(self):
        d = mmdict.CaselessMultiDict(aliases={"Test": ["check", "assert"]})
        d["tesT"] = "ok"
        # We should get the key that we provided in the alias names rather
        # than the name given on the first write.
        self.assertCountEqual(d.keys(), ["Test"])

        # The name should persist if we empty and re-fill the dict without
        # removing the alias
        del d["Test"]
        self.assertEqual(len(d), 0)
        d["assert"] = "ok"
        self.assertCountEqual(d.keys(), ["Test"])

    def test__alias_defined_then_unaliased_external_names_persist_until_values_are_removed(self):
        d = mmdict.CaselessMultiDict(aliases={"Test": "check"})
        d["tesT"] = "ok"
        d.unalias("check")
        self.assertCountEqual(d.keys(), ["Test"])

        # Once we remove the value from the previously alias-defined external name
        # `Test`, and write to it a second time, the second spelling will become the
        # external name.
        del d["Test"]
        d["TesT"] = "ok"
        self.assertCountEqual(d.keys(), ["TesT"])


if __name__ == '__main__':
    unittest.main()
