import unittest

from jsonrpc_pyclient.error import JsonRpcError


class TestError(unittest.TestCase):
    def test_raise_JsonRpcError(self):
        with self.assertRaises(JsonRpcError):
            self.raise_JsonRpcError()

    def raise_JsonRpcError(self):
        raise JsonRpcError(-32600, 'Invalid Request')
