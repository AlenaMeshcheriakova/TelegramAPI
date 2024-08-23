from google.protobuf import empty_pb2
from src.grpc.group_service import group_service_pb2_grpc, group_service_pb2
from concurrent import futures
import grpc

class MockGroupService(group_service_pb2_grpc.GroupServiceServicer):
    """
    Mock behavior for methods in GroupService
    """
    def get_groups_name_by_user_name(self, request, context):
        return group_service_pb2.GetGroupsNameByUserNameResponse(
            group_names=['group1', 'group2', 'group3']
        )

    def create_group(self, request, context):
        return empty_pb2.Empty()

    def get_group_id_by_group_name(self, request, context):
        return group_service_pb2.GetGroupIdByGroupNameResponse(
            group_id='123e4567-e89b-12d3-a456-426614174000'
        )

    def is_group_created(self, request, context):
        created = request.group_name in ['group1', 'group2', 'group3']
        return group_service_pb2.IsGroupCreatedResponse(
            created=created
        )

def serve(stop_event):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    group_service_pb2_grpc.add_GroupServiceServicer_to_server(MockGroupService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # server.wait_for_termination()

    def wait_for_stop():
        stop_event.wait()
        server.stop(grace=None)  # Stop the server without waiting for ongoing requests to complete

    return server, wait_for_stop