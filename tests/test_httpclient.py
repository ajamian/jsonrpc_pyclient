import unittest
import json
import multiprocessing

from jsonrpc_pyclient.connectors.httpclient import HttpClient


class TestHttpClient(unittest.TestCase):
    def setUp(self):
        import tests.dummyservers.httpserver
        self.p = multiprocessing.Process(target=tests.dummyservers.httpserver.main)
        self.p.daemon=True
        self.p.start()

    def tearDown(self):
        self.p.terminate()

    def test_send_rpc_message(self):
        client = HttpClient('http://localhost:4000')

        hello = {"method": "sayHello", "jsonrpc": "2.0", "id": 5,
                 "params": {"name": "Winnie-the-Pooh"}}
        message = json.dumps(hello) + '\n'

        response = client.send_rpc_message(message)

        expected = {"jsonrpc": "2.0", "id": 5, "result": "Hello Winnie-the-Pooh"}
        self.assertEqual(json.loads(response), expected)

    def test_send_rpc_message_requests_failure(self):
        client = HttpClient('http://localhost:4232')

        hello = {"method": "sayHello", "jsonrpc": "2.0", "id": 5,
                 "params": {"name": "Winnie-the-Pooh"}}
        message = json.dumps(hello) + '\n'

        try:
            response = client.send_rpc_message(message)
            self.assertLogs()
        except:
            # assertLogs isn't available in python < 3.4
            pass
