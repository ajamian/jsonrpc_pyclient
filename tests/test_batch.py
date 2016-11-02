import unittest
import json

from jsonrpc_pyclient.batch import BatchRequest
from jsonrpc_pyclient.batch import BatchResponse

class TestBatchRequest(unittest.TestCase):

    def test_add_call(self):
        batchrequest = BatchRequest()

        method = 'test'
        parameters = [1, 5]
        is_notification = False

        call_id = batchrequest.add_call(method, parameters, is_notification)

        expected = [{"jsonrpc": "2.0", "method": method, "params": parameters, "id": call_id}]
        self.assertEqual(batchrequest.calls, expected)

    def test_add_call_notification(self):
        batchrequest = BatchRequest()

        method = 'test'
        parameters = [1, 5]
        is_notification = True

        call_id = batchrequest.add_call(method, parameters, is_notification)

        expected = [{"jsonrpc": "2.0", "method": method, "params": parameters}]
        self.assertEqual(batchrequest.calls, expected)

    def test_format_request(self):
        batchrequest = BatchRequest()

        method = 'test'
        parameters = [1, 5]
        is_notification = False

        call_id = batchrequest.add_call(method, parameters, is_notification)
        expected = json.dumps(batchrequest.calls) + '\n'
        self.assertEqual(batchrequest.format_request(), expected)

    def test_str(self):
        batchrequest = BatchRequest()

        method = 'test'
        parameters = [1, 5]
        is_notification = False

        call_id = batchrequest.add_call(method, parameters, is_notification)

        self.assertEqual(batchrequest.__str__(), str(batchrequest.calls))



class TestBatchResponse(unittest.TestCase):

    def  test_add_result(self):
        batchresponse = BatchResponse()

        response = {"jsonrpc": "2.0", "result": 19, "id": 1}
        result = {1: 19}

        batchresponse.add_result(response)
        self.assertEqual(batchresponse.results, result)

    def test_add_result_error(self):
        batchresponse = BatchResponse()

        response = {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": 1}
        result = {1: {"code": -32600, "message": "Invalid Request"}}

        batchresponse.add_result(response)
        self.assertEqual(batchresponse.results, result)

    def test_get_result(self):
        batchresponse = BatchResponse()

        response = {"jsonrpc": "2.0", "result": 19, "id": 1}

        batchresponse.add_result(response)
        self.assertEqual(batchresponse.get_result(1), 19)

    def test_get_result_invalid_id(self):
        batchresponse = BatchResponse()

        response = {"jsonrpc": "2.0", "result": 19, "id": 1}

        batchresponse.add_result(response)
        self.assertEqual(batchresponse.get_result(5), None)

    def test_str(self):
        batchresponse = BatchResponse()

        response = {"jsonrpc": "2.0", "result": 19, "id": 1}

        batchresponse.add_result(response)
        self.assertEqual(batchresponse.__str__(), str(batchresponse.results))

    def test_process_batch(self):
        responses = ('[{"jsonrpc": "2.0", "result": 19, "id": 1},'
                     '{"jsonrpc": "2.0", "result": "test", "id": 2},'
                     '{"jsonrpc": "2.0", "result": 12.12, "id": 5}]'
                    )

        batchresponse = BatchResponse()

        batchresponse.process_batch(responses)

        expected = {1: 19, 2: 'test', 5: 12.12}
        self.assertEqual(batchresponse.results, expected)

    def test_process_batch_invalid_string(self):
        responses = ('[{"jsonrpffc":adf "2.0", "result": 19, "id": 1},'
                     '{"jsonrpc": "2.0",9420 "result": "test", "id": 2},asdff388'
                     '{"jsonrpc": "2.0"fee, "result": 12.12, "id": 5}]'
                    )

        batchresponse = BatchResponse()
        batchresponse.process_batch(responses)

        try:
            self.assertLogs()
        except:
            # assertLogs isn't available in python < 3.4
            pass
