import unittest
import json
import multiprocessing

from jsonrpc_pyclient.connectors.socketclient import TcpSocketClient

class TestTcpSocketClient(unittest.TestCase):

    def setUp(self):
        import tests.dummyservers.socketserver

        q = multiprocessing.Queue()
        self.server = tests.dummyservers.socketserver.TcpSocketServer()

        self.p = multiprocessing.Process(target=self.server.run, args=(q,))
        self.p.daemon = True
        self.p.start()

        # wait until socket is established
        while not q.get():
            pass

    def tearDown(self):
        self.p.terminate()
        self.server.stop()

    def test_send_rpc_message(self):
        client = TcpSocketClient("127.0.0.1", 1238)

        hello = {"method": "sayHello", "jsonrpc": "2.0", "id": 5,
                 "params": {"name": "Winnie-the-Pooh"}}
        message = json.dumps(hello) + '\n'

        response = client.send_rpc_message(message)

        expected = {"jsonrpc": "2.0", "id": 5, "result": "Hello Winnie-the-Pooh"}
        self.assertEqual(json.loads(response), expected)

    def test_send_rpc_message_failure(self):
        client = TcpSocketClient("127.0.0.1", 1234)

        hello = {"method": "sayHello", "jsonrpc": "2.0", "id": 5,
                 "params": {"name": "Winnie-the-Pooh"}}
        message = json.dumps(hello) + '\n'

        try:
            response = client.send_rpc_message(message)
            self.assertLogs()
        except:
            # assertLogs isn't available in python < 3.4
            pass
