import unittest

from app.irma_api import db
import app.irma as irma
import app.db_operations as db_ops


class IrmaTest(unittest.TestCase):
    def test_check_sign_valid(self):
        self.assertEqual("aries", irma.check_sign("aries"))
        self.assertEqual("aries", irma.check_sign("ARIes"))

    def test_check_sign_invalid(self):
        with self.assertRaises(Exception):
            irma.check_sign("invalid")

    def test_read_future_valid(self):
        self.assertEqual("Are those horns?", db_ops.read_future("aries", db))

    def test_read_future_invalid(self):
        self.assertEqual("no future", db_ops.read_future("non-existing", db))

    def test_see_future_valid(self):
        expected = "\n    Aries, your future is:\n    Are those horns?\n    "
        res = irma.see_future("aries", db)
        self.assertEqual(expected, res)

    def test_see_future_invalid(self):
        with self.assertRaises(Exception):
            irma.see_future("invalid", db)


if __name__ == "__main__":
    unittest.main()
