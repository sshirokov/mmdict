import unittest

import mmdict

class MultiDictAliasTests(unittest.TestCase):
    def test__can_delete_value_through_alias(self):
        data = {"test": "ok"}
        aliases = {"test": ["also", "as well"]}
        d = mmdict.MultiDict(data, aliases)

        del d["also"]
        self.assertIsNone(d.get("test"))
        self.assertFalse("test" in d)
        self.assertFalse("also" in d)

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

    def test__declare_and_read_through_single_alias_using_constructor_alias_kwargs(self):
        data = {"test": "ok"}
        aliases = {"test": "also"}
        d = mmdict.MultiDict(data, aliases=aliases)

        self.assertEqual(d["also"], "ok")

    def test__declare_and_read_through_single_alias_using_constructor_alias_kwargs_only(self):
        aliases = {"test": "also"}
        d = mmdict.MultiDict(aliases=aliases)
        d["test"] = "ok"
        self.assertEqual(d["also"], "ok")

    def test__will_not_allow_two_aliases_to_collide(self):
        bad_aliases = {
            "first": ["first1", "duplicate"],
            "second": ["second1", "duplicate"],
        }

        with self.assertRaises(mmdict.AliasExistsError):
            d = mmdict.MultiDict({}, aliases=bad_aliases)

    def test__will_not_allow_two_aliases_to_collide_singluar_keys(self):
        bad_aliases = {
            "first": "duplicate",
            "second": "duplicate",
        }

        with self.assertRaises(mmdict.AliasExistsError):
            d = mmdict.MultiDict({}, aliases=bad_aliases)

    def test__alias_cannot_shadow_another_alias_destiation(self):
        bad_aliases = {
            "first": ["second"],
            "second": ["first"],
        }
        with self.assertRaises(mmdict.AliasExistsError):
            d = mmdict.MultiDict(aliases=bad_aliases)

    def test__KeyError_for_alias_includes_requested_key(self):
        bad_key_name = "bad-key-name"
        d = mmdict.MultiDict(
            {"test": "ok"},
            {"does-not-exist": bad_key_name}
        )

        self.assertEqual(d["test"], "ok")
        with self.assertRaisesRegex(KeyError, bad_key_name):
            d[bad_key_name]

    def test__can_unalias_existing_aliases(self):
        data = {"test": "ok"}
        aliases = {"test": ["check", "evaluate"]}
        d = mmdict.MultiDict(data, aliases)

        self.assertEqual(d["test"], d["check"])
        self.assertEqual(d["evaluate"], d["check"])

        self.assertTrue(d.unalias("evaluate"))
        self.assertIsNone(d.get("evaluate"))
        self.assertFalse("evaluate" in d)
        self.assertFalse(d.unalias("evaluate"))

    def test__constructor_writes_follow_alias_definitions(self):
        data = {"also": "ok"}
        aliases = {"test": ["also", "as well", "furthermore"]}
        d = mmdict.MultiDict(data, aliases=aliases)

        self.assertEqual(d['test'], "ok")
        self.assertEqual(d["also"], "ok")
        self.assertEqual(d['as well'], "ok")

    def test__writes_follow_alias_definitions(self):
        aliases = {"test": ["also", "as well", "furthermore"]}
        d = mmdict.MultiDict(aliases=aliases)

        d["furthermore"] = "ok"
        self.assertEqual(d['test'], "ok")
        self.assertEqual(d["also"], "ok")
        self.assertEqual(d['as well'], "ok")

    def test__clear_alias_for_canonical_key(self):
        pass_aliases = ["yes", "succeed", "hooray"]
        aliases = {
            "test": ["also", "as well", "furthermore"],
            "pass": pass_aliases,
        }
        data = {
            "pass": "ok",
            "test": "also ok"
        }
        d = mmdict.MultiDict(data, aliases=aliases)

        # We can read it before we clear
        self.assertEqual(d["yes"], "ok")

        # Then make sure we cannot read any of the aliases after we clear
        d.unalias_all("pass")
        for alias in pass_aliases:
            self.assertFalse(alias in d)
            self.assertIsNone(d.get(alias))
            with self.assertRaises(KeyError):
                d[alias]

        # But can read the canonical key
        self.assertEqual(d["pass"], "ok")
        # And it doesn't break other aliases
        self.assertEqual(d["furthermore"], d["test"])

    def test__can_return_regular_dict_with_canonical_keys(self):
        expected = {
            "first": "ok",
            "second": "fine",
            "third": "great",
        }
        d = mmdict.MultiDict(aliases={
            "first": [1, "1st", "one"],
            "second": [2, "2nd", "two"],
            "third": "three"
        })
        d.update({
            "third": "great",
            "2nd": "fine",
            1: "ok"
        })

        regular_d = d.to_dict()
        self.assertDictEqual(expected, regular_d)


if __name__ == '__main__':
    unittest.main()
