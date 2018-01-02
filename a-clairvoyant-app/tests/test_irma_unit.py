import unittest

import app.irma as irma


class IrmaTest(unittest.TestCase):
    def test_check_sign_valid(self):
        self.assertEqual("aries", irma.check_sign("aries"))
        self.assertEqual("aries", irma.check_sign("ARIes"))

    def test_check_sign_invalid(self):
        with self.assertRaises(Exception):
            irma.check_sign("invalid")

    def test_read_future_valid(self):
        self.assertEqual("Are those horns?", irma.read_future("aries"))

    def test_read_future_invalid(self):
        self.assertEqual("no future", irma.read_future("non-existing"))

    def test_see_future_valid(self):
        expected = "\n    Aries, your future is:\n    Are those horns?\n    "
        res = irma.see_future("aries")
        self.assertEqual(expected, res)

    def test_see_future_invalid(self):
        with self.assertRaises(Exception):
            irma.see_future("invalid")


if __name__ == "__main__":
    unittest.main()
