from datetime import datetime

from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp

from src.grpc.level_service import level_service_pb2, level_service_pb2_grpc

from uuid import uuid4
import grpc
from concurrent import futures

class MockLevelService(level_service_pb2_grpc.LevelServiceGRPCServicer):
    def create_levels(self, request, context):
        return empty_pb2.Empty()  # Return an empty response as per proto definition

    def get_levels(self, request, context):
        levels = [
            level_service_pb2.LevelDTO(
                lang_level=level_service_pb2.LevelEnum.A1,
                created_at=Timestamp(seconds=int(datetime.now().timestamp())),
                updated_at=Timestamp(seconds=int(datetime.now().timestamp()))
            ),
            level_service_pb2.LevelDTO(
                lang_level=level_service_pb2.LevelEnum.A2,
                created_at=Timestamp(seconds=int(datetime.now().timestamp())),
                updated_at=Timestamp(seconds=int(datetime.now().timestamp()))
            )
        ]
        return level_service_pb2.LevelList(levels=levels)

    def get_level_id_by_name(self, request, context):
        # Simulate returning a UUID for a level
        level_ids = {
            level_service_pb2.LevelEnum.A1: '123e4567-e89b-12d3-a456-426614174000',
            level_service_pb2.LevelEnum.A2: '123e4567-e89b-12d3-a456-426614174001'
        }
        level_id = level_ids.get(request.level_enum, str(uuid4()))
        return level_service_pb2.LevelIdResponse(id=level_id)

def serve(stop_event):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    level_service_pb2_grpc.add_LevelServiceGRPCServicer_to_server(MockLevelService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    def wait_for_stop():
        stop_event.wait()
        server.stop(grace=None)

    return server, wait_for_stop