import unittest

from app.api_management import api_connection_check


class TestAPIConnection(unittest.TestCase):

    def test_successful_connection(self):
        self.assertEqual(api_connection_check(), 200)


if __name__ == "__main__":
    unittest.main()
