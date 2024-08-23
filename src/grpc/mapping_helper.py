from typing import Type, Any, Dict, TypeVar
from google.protobuf import timestamp_pb2
from google.protobuf.internal.well_known_types import Timestamp
from pydantic import BaseModel
import uuid
from datetime import datetime
from src.model.level_enum import LevelEnum
from src.model.word_type_enum import WordTypeEnum

# Define type variables for generic conversion
PydanticModelType = TypeVar('PydanticModelType', bound=BaseModel)
ProtoMessageType = TypeVar('ProtoMessageType')

def datetime_to_timestamp(dt: datetime) -> timestamp_pb2.Timestamp():
    """Convert a datetime object to a google.protobuf.Timestamp object."""
    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(dt)
    return ts

def parse_timestamp(proto_timestamp: Timestamp) -> datetime:
    """Converts a Protobuf Timestamp to a Python datetime object."""
    return datetime.fromtimestamp(proto_timestamp.seconds + proto_timestamp.nanos / 1e9)

def parse_value(value: Any, target_type: Type) -> Any:
    """Converts a value to the target_type, handling common types."""
    if target_type == datetime and isinstance(value, Timestamp):
        return parse_timestamp(value)
    elif target_type == uuid.UUID and isinstance(value, str):
        return uuid.UUID(value)
    elif target_type == str and isinstance(value, bytes):
        return value.decode('utf-8')
    return value


def get_annotations(pydantic_model: Type[BaseModel]):
    """Get annotations from the Pydantic model and its superclasses."""
    annotations = {}

    # Traverse the class hierarchy
    for cls in pydantic_model.mro():
        if issubclass(cls, BaseModel) and cls is not BaseModel:
            annotations.update(cls.__annotations__)

    return annotations

def convert_protobuf_level_enum_to_python_enum(protobuf_enum_value: int) -> LevelEnum:
    mapping = {
        1: LevelEnum.a1,
        2: LevelEnum.a2,
        3: LevelEnum.b1,
        4: LevelEnum.b2,
        5: LevelEnum.c1,
        6: LevelEnum.c2
    }
    return mapping.get(protobuf_enum_value)

def convert_protobuf_word_type_enum_to_python_enum(protobuf_enum_value: int) -> WordTypeEnum:
    mapping = {
        1: WordTypeEnum.standard,
        2: WordTypeEnum.custom,
        3: WordTypeEnum.test
    }
    return mapping.get(protobuf_enum_value)
def convert_proto_to_pydantic(proto_msg: Any, pydantic_model: Type[BaseModel]) -> BaseModel:
    """Converts a Protobuf message to a Pydantic model."""
    pydantic_fields = get_annotations(pydantic_model)
    pydantic_data = {}

    for field_name, field_type in pydantic_fields.items():
        if hasattr(proto_msg, field_name):
            proto_value = getattr(proto_msg, field_name)
            pydantic_data[field_name] = parse_value(proto_value, field_type)

    return pydantic_model(**pydantic_data)

def pydantic_to_protobuf(pydantic_model: Any, protobuf_class: Type[Any], field_mapping: Dict[str, str]) -> Any:
    """Convert a Pydantic model to a Protobuf message based on a field mapping."""

    # Create an instance of the Protobuf message
    proto_message = protobuf_class()

    for pydantic_field, protobuf_field in field_mapping.items():
        value = getattr(pydantic_model, pydantic_field, None)

        if isinstance(value, datetime):
            timestamp = datetime_to_timestamp(value)
            if protobuf_field == "created_at":
                proto_message.created_at.CopyFrom(timestamp)
            elif protobuf_field == "updated_at":
                proto_message.updated_at.CopyFrom(timestamp)
            else:
                proto_message.__setattr__(protobuf_field, timestamp)
        elif isinstance(value, uuid.UUID):
            setattr(proto_message, protobuf_field, str(value))
        elif isinstance(value, str):
            # Handle StringValue wrapper field
            setattr(proto_message, protobuf_field, value)
        elif isinstance(value, bool):
            # Handle BoolValue wrapper field
            setattr(proto_message, protobuf_field, value)
        elif value is None:
            proto_message.ClearField(protobuf_field)
        else:
            # Direct assignment for other types
            setattr(proto_message, protobuf_field, value)
    return proto_message