import unittest

import mmdict

class BasicTests(unittest.TestCase):
    def test_can_instantiate_empty_MultiDict(self):
        d = mmdict.MultiDict()
        self.assertIsNotNone(d)

