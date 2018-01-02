import os
import subprocess
import unittest


class IrmaIntegrationTest(unittest.TestCase):
    def test_irma_valid(self):
        expected = "\n    Aries, your future is:\n    Are those horns?\n    \n"
        res = subprocess.check_output(["python",
                                       os.getcwd() + "/app/irma.py",
                                       "aries"])
        self.assertEqual(expected, res)


if __name__ == "__main__":
    unittest.main()
