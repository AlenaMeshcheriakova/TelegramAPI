import uuid
from concurrent import futures

import grpc
from google.protobuf import empty_pb2

from src.grpc.word_service import word_service_pb2, word_service_pb2_grpc

class MockWordService(word_service_pb2_grpc.WordServiceServicer):
    def get_words_by_user(self, request, context):
        words = [
            word_service_pb2.GetWordsByUserResponse(
                user_id=request.user_id,
                german_word="Hallo",
                english_word="Hello",
                russian_word="Привет",
                amount_already_know=3,
                amount_back_to_learning=1,
                lang_level_id=str(uuid.uuid4()),
                word_type_id=str(uuid.uuid4()),
                group_id=str(uuid.uuid4())
            )
        ]
        return word_service_pb2.GetListWordsByUserResponse(words=words)

    def add_new_word_from_dto(self, request, context):
        return empty_pb2.Empty()

    def add_new_word(self, request, context):
        return empty_pb2.Empty()

def serve(stop_event):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    word_service_pb2_grpc.add_WordServiceServicer_to_server(MockWordService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    def wait_for_stop():
        stop_event.wait()
        server.stop(grace=None)

    return server, wait_for_stop
