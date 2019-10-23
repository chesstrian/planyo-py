from json import JSONDecodeError

import requests


class Planyo(object):
    """
    Planyo API low level client. Provides a straightforward mapping from
    Python to Planyo REST endpoint.

      >>> from planyo import Planyo
      >>> client = Planyo(api_key='ABC')
      >>> client.api_test()
    """

    endpoint = "https://api.planyo.com/rest/"
    methods = (
        # Check
        'api_test',
    )

    def __init__(self, api_key):
        """
        :param api_key: Planyo API key
        """
        self.api_key = api_key

    def _get_hash_key(self, ts, method):
        """
        Calculate hash key

        :param ts: Timestamp
        :param method: Function name
        :return: Hash key
        """
        raise NotImplementedError

    def _wrapper(self, method):
        args = dict(method=method, api_key=self.api_key)

        def perform_request(params=None, retry=3):
            if params:
                params.update(args)
            else:
                params = args

            try:
                response = requests.post(self.endpoint, data=params)
            except (requests.ReadTimeout, requests.ConnectTimeout, requests.ConnectionError):
                if retry > 0:
                    return self._perform_request(params, retry=retry - 1)

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


__all__ = ('Planyo',)
