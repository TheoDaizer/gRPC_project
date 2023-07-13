from concurrent import futures
import logging
import grpc

import grsp_project_pb2
import grsp_project_pb2_grpc

from grps_project_postgres_connection import create_connection,\
    select, insert, update, connection_data


class GetData(grsp_project_pb2_grpc.GetDataServicer):

    def __base_seleck_query(self, condition_columns, condition_data):
        connection = create_connection(*connection_data.values())
        query_result = select(['id', 'name', 'quantity'], condition_columns,
                              condition_data, 'products', connection)
        # TODO необходимо передавать поток и убрать костыль для пустого запроса
        if len(query_result) == 0:
            return grsp_project_pb2.GetDatatReply(id=-1, name='', quantity=0)
        else:
            result = query_result[0]
            return grsp_project_pb2.GetDatatReply(id=result[0], name=result[1], quantity=result[2])

    def SelectByName(self, request, context):
        return self.__base_seleck_query(['name'], [request.name])

    def SelectByID(self, request, context):
        return self.__base_seleck_query(['id'], [request.id])

    def SelectByQuantity(self, request, context):
        return self.__base_seleck_query(['quantity'], [request.quantity])


class SetData(grsp_project_pb2_grpc.SetDataServicer):

    def Insert(self, request, context):
        connection = create_connection(*connection_data.values())
        data = [request.name, request.quantity]
        insert(['name', 'quantity'], data, 'products', connection)
        return grsp_project_pb2.SetDataReply(status='done')

    def Update(self, request, context):
        connection = create_connection(*connection_data.values())
        update_data = [request.name, request.quantity]
        update(['name', 'quantity'], update_data, ['id'], [request.id], 'products', connection)

        return grsp_project_pb2.SetDataReply(status='done')


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grsp_project_pb2_grpc.add_GetDataServicer_to_server(GetData(), server)
    grsp_project_pb2_grpc.add_SetDataServicer_to_server(SetData(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()