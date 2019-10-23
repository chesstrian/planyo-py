from datetime import datetime
from hashlib import md5
from json import JSONDecodeError

import requests


class Planyo(object):
    """
    Planyo API low level client. Provides a straightforward mapping from
    Python to Planyo REST endpoint.

      >>> from planyo import Planyo
      >>> client = Planyo(api_key='ABC')
      >>> client.api_test()

    The instance has all methods in Planyo API Docs: https://api.planyo.com/api.php
    It is highly recommended to checks docs for params received by any method. Just pass a dictionary in `params` with
    all desired arguments.

      >>> client.list_translations(params=dict(language='IT'))

    Hash key is also supported, in this case the instance needs to be initialized with the secret hash key from Planyo

      >>> client = Planyo(api_key='ABC', hash_key='DEF')
      >>> client.list_translations(is_hash_enabled=True)
    """

    endpoint = "https://api.planyo.com/rest/"
    methods = (
        # Check
        'api_test',
    )

    def __init__(self, api_key, hash_key=None):
        """
        :param api_key: Planyo API key
        :param hash_key: Planyo secret hash key
        """
        self.api_key = api_key
        self.hash_key = hash_key

    def _get_hash_key(self, ts, method):
        """
        Calculate hash key

        :param ts: Timestamp
        :param method: Function name
        :return: MD5 hash
        """
        if not self.hash_key:
            raise InvalidHashKeyException
        return md5(f'{self.hash_key}{ts}{method}'.encode()).hexdigest()

    def _wrapper(self, method):
        def perform_request(params=None, is_hash_enabled=False, retry=3):
            args = dict(method=method, api_key=self.api_key)
            if is_hash_enabled:
                ts = int(datetime.utcnow().timestamp())
                args.update(hash_timestamp=ts, hash_key=self._get_hash_key(ts, method))

            if params:
                params.update(args)
            else:
                params = args

            try:
                response = requests.post(self.endpoint, data=params)
            except (requests.ReadTimeout, requests.ConnectTimeout, requests.ConnectionError):
                if retry > 0:
                    return self._perform_request(params, is_hash_enabled, retry=retry - 1)

                raise ServerConnectionLostException

            try:
                return response.json()
            except JSONDecodeError as e:
                raise e

        return perform_request

    def __getattr__(self, item):
        if item in self.methods:
            return self._wrapper(method=item)


class ServerConnectionLostException(Exception):
    """
    Planyo API Server is Down
    """


class InvalidHashKeyException(Exception):
    """
    Invalid Hash Key provided
    """


__all__ = ('Planyo',)
