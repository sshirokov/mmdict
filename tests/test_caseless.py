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

if __name__ == '__main__':
    unittest.main()
