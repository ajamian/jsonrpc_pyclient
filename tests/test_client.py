import unittest

from jsonrpc_pyclient.client import Client
from jsonrpc_pyclient.connectors.socketclient import TcpSocketClient

class TestClient(unittest.TestCase):

    def setUp(self):
        import multiprocessing

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

    def test_call_method_v2(self):
        connector = TcpSocketClient('127.0.0.1', 1238)
        client = Client(connector)
        result = client.call_method('sayHello', {'name': 'Thelonious'})
        expected = 'Hello Thelonious'
        self.assertEqual(result, expected)

    def test_call_method_v1(self):
        connector = TcpSocketClient('127.0.0.1', 1238)
        client = Client(connector, '1.0')
        result = client.call_method('sayHello', {'name': 'Thelonious'})
        expected = 'Hello Thelonious'
        self.assertEqual(result, expected)

    def test_call_procedures(self):
        from jsonrpc_pyclient.batch import BatchRequest
        from jsonrpc_pyclient.batch import BatchResponse

        connector = TcpSocketClient('127.0.0.1', 1238, 1024)
        client = Client(connector)

        batchcall = BatchRequest()
        steveId = batchcall.add_call('sayHello', {'name': 'Steve'}, False)
        batchcall.add_call('notifyServer', None, True)
        adamId = batchcall.add_call('sayHello', {'name': 'Adam'}, False)

        responses = client.call_procedures(batchcall)
        result1 = responses.get_result(steveId)
        result2 = responses.get_result(adamId)

        self.assertEqual(result1, 'Hello Steve')
        self.assertEqual(result2, 'Hello Adam')
