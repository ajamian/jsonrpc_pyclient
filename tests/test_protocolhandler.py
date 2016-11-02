import unittest
import json

from jsonrpc_pyclient.protocolhandler import RpcProtocolHandler

class TestRpcProtocolHandler(unittest.TestCase):

    def setUp(self):
        self.protocolv2 = RpcProtocolHandler('2.0')
        self.protocolv1 = RpcProtocolHandler('1.0')

    def test_build_v2_request_list(self):
        method = 'test'
        parameters = [1, 4, 'testing']
        is_notification = False

        request, request_id = self.protocolv2.build_request(method, parameters, is_notification)
        expected = {"jsonrpc": "2.0", "method": method, "params": parameters, "id": request_id}

        # Since the key order of the json string isn't guaranteed to match,
        # we load the string into a json object, that way order doesn't matter.
        self.assertEqual(json.loads(request), expected)

    def test_build_v2_request_notification(self):
        method = 'test'
        parameters = None
        is_notification = True

        request, request_id = self.protocolv2.build_request(method, parameters, is_notification)
        expected = {"jsonrpc": "2.0", "method": method}

        # Since the key order of the json string isn't guaranteed to match,
        # we load the string into a json object, that way order doesn't matter.
        self.assertEqual(json.loads(request), expected)

    def test_build_v2_request_dictionary(self):
        method = 'test'
        parameters = {"name": "bob", "number": 3}
        is_notification = False

        request, request_id = self.protocolv2.build_request(method, parameters, is_notification)
        expected = {"jsonrpc": "2.0", "method": method, "params": parameters, "id": request_id}

        # Since the key order of the json string isn't guaranteed to match,
        # we load the string into a json object, that way order doesn't matter.
        self.assertEqual(json.loads(request), expected)

    def test_build_v1_request_list(self):
        method = 'test'
        parameters = [1, 4, 'testing']
        is_notification = False

        request, request_id = self.protocolv1.build_request(method, parameters, is_notification)
        expected = {"method": method, "params": parameters, "id": request_id}

        # Since the key order of the json string isn't guaranteed to match,
        # we load the string into a json object, that way order doesn't matter.
        self.assertEqual(json.loads(request), expected)

    def test_build_v1_request_notification(self):
        method = 'test'
        parameters = None
        is_notification = True

        request, request_id = self.protocolv1.build_request(method, parameters, is_notification)
        expected = {"method": method, "id": None}

        # Since the key order of the json string isn't guaranteed to match,
        # we load the string into a json object, that way order doesn't matter.
        self.assertEqual(json.loads(request), expected)

    def test_build_v1_request_dictionary(self):
        method = 'test'
        parameters = {"name": "bob", "number": 3}
        is_notification = False

        request, request_id = self.protocolv1.build_request(method, parameters, is_notification)
        expected = {"method": method, "params": parameters, "id": request_id}

        # Since the key order of the json string isn't guaranteed to match,
        # we load the string into a json object, that way order doesn't matter.
        self.assertEqual(json.loads(request), expected)

    def test_handle_response_valid_string(self):
        response = '{"jsonrpc": "2.0", "result": "test_result", "id": 0}'

        result = self.protocolv2.handle_response(response)
        self.assertEqual(result, json.loads(response)['result'])

        result = self.protocolv1.handle_response(response)
        self.assertEqual(result, json.loads(response)['result'])

    def test_handle_response_invalid_string(self):
        response = '{"jsonrpc": "2.0", "result":0123 "test_result", "id": 0}'

        # Handle_response is the same for protocolv2 and protocolv1.
        result = self.protocolv2.handle_response(response)
        try:
            self.assertLogs()
        except:
            # assertLogs isn't available in python < 3.4
            pass

    def test_handle_response_jsonrpc_error(self):
        from jsonrpc_pyclient.error import JsonRpcError

        response = '{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": "1"}'

        with self.assertRaises(JsonRpcError):
            result = self.protocolv2.handle_response(response)

if __name__ == '__main__':
    unittest.main()
