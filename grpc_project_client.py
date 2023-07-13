from __future__ import print_function

import logging

import grpc
import grsp_project_pb2
import grsp_project_pb2_grpc


def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grsp_project_pb2_grpc.GetDataStub(channel)
        response = stub.SelectByID(grsp_project_pb2.GetDataRequest(id=1))

        print(f"Client received: \n\tid = {response.id},"
              f" \n\tname = {response.name}, \n\tquantity = {response.quantity}\n")

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = grsp_project_pb2_grpc.SetDataStub(channel)
        res2 = stub.Update(grsp_project_pb2.SetDataRequest(id=11, name='something', quantity=11))
        print(f'Status: {res2.status}')


if __name__ == '__main__':
    logging.basicConfig()
    run()