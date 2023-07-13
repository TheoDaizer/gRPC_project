import unittest
from concurrent import futures
import grpc

from grpc_project_server import GetData, SetData
import grsp_project_pb2_grpc
import grsp_project_pb2


class GetDataTest(unittest.TestCase):
    server_class = GetData
    port = 50051

    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        grsp_project_pb2_grpc.add_GetDataServicer_to_server(self.server_class(), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()

    def tearDown(self):
        self.server.stop(None)

    def test_select_id(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = grsp_project_pb2_grpc.GetDataStub(channel)
            response = stub.SelectByID(grsp_project_pb2.GetDataRequest(id=1))
        self.assertEqual(response.name, 'book')

    def test_select_name(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = grsp_project_pb2_grpc.GetDataStub(channel)
            response = stub.SelectByName(grsp_project_pb2.GetDataRequest(name='book'))
        self.assertEqual(response.id, 1)

    def test_select_quantity(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = grsp_project_pb2_grpc.GetDataStub(channel)
            response = stub.SelectByQuantity(grsp_project_pb2.GetDataRequest(quantity=10))
        self.assertEqual(response.id, 1)


class SetDataTest(unittest.TestCase):
    server_class = SetData
    port = 50051

    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        grsp_project_pb2_grpc.add_SetDataServicer_to_server(self.server_class(), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()

    def tearDown(self):
        self.server.stop(None)

    def test_input(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = grsp_project_pb2_grpc.SetDataStub(channel)
            response = stub.Insert(grsp_project_pb2.SetDataRequest(name='oil', quantity=65))
        self.assertEqual(response.status, 'done')

    def test_update(self):
        with grpc.insecure_channel(f'localhost:{self.port}') as channel:
            stub = grsp_project_pb2_grpc.SetDataStub(channel)
            response = stub.Update(grsp_project_pb2.SetDataRequest(id=1, name='book', quantity=10))
        self.assertEqual(response.status, 'done')


if __name__ == '__main__':
    unittest.main()
