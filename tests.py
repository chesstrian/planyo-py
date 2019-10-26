import unittest
from random import choice

from planyo import Planyo


class PlanyoTests(unittest.TestCase):
    def setUp(self):
        self.client = Planyo(api_key='ABC')

    def test_valid_method(self):
        method = choice(Planyo.methods)
        self.assertIsNotNone(self.client.__getattr__(method))

    def test_invalid_method(self):
        method = 'non_existing_method'
        self.assertIsNone(self.client.__getattr__(method))

    def test_hash_key(self):
        self.client.hash_key = 'DEF'
        self.assertEqual('fcec20584eef39f4f565a3273f56b33f', self.client._get_hash_key('1572051750', 'api_test'))

        del self.client.hash_key

    def test_valid_request(self):
        response = {
            'data': 'API Test Response',
            'response_code': 0,
            'response_message': 'Method api_test executed successfully.'
        }
        self.assertEqual(response, self.client.api_test())

    def test_invalid_request(self):
        response = {
            'response_code': 1,
            'response_message': 'Invalid method or API key for specified Planyo site'
        }
        self.assertEqual(response, self.client.list_translations())


if __name__ == '__main__':
    unittest.main()
