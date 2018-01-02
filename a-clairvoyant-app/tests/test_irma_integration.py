import unittest
import requests


class IrmaIntegrationTest(unittest.TestCase):
    def test_irma_valid(self):
        res = requests.get('http://127.0.0.1:5000/irma/aries')
        self.assertEqual(200, res.status_code)

        expected = "\n    Aries, your future is:\n    Are those horns?\n    "
        self.assertEqual(expected, res.text)


if __name__ == "__main__":
    unittest.main()
