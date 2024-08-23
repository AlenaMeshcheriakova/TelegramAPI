from concurrent import futures
from uuid import uuid4
import grpc
from src.grpc.word_type_service import word_type_service_pb2, word_type_service_pb2_grpc

class MockWordTypeService(word_type_service_pb2_grpc.WordTypeServiceServicer):
    def get_word_type_id(self, request, context):
        # Simulate UUID responses for different word types
        word_type_ids = {
            word_type_service_pb2.WordTypeEnum.STANDARD: '123e4567-e89b-12d3-a456-426614174001',
            word_type_service_pb2.WordTypeEnum.CUSTOM: '123e4567-e89b-12d3-a456-426614174002',
            word_type_service_pb2.WordTypeEnum.TEST_WORD_TYPE: '123e4567-e89b-12d3-a456-426614174000'
        }
        word_type_id = word_type_ids.get(request.word_type, str(uuid4()))
        return word_type_service_pb2.GetWordTypeIdResponse(word_type_id=word_type_id)

def serve(stop_event):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    word_type_service_pb2_grpc.add_WordTypeServiceServicer_to_server(MockWordTypeService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    def wait_for_stop():
        stop_event.wait()
        server.stop(grace=None)

    return server, wait_for_stop