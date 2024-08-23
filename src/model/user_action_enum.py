import enum

class UserActionEnum(str, enum.Enum):
    ALREADY_KNOW = "ALREADY_KNOW"
    BACK_TO_LEARNING = "BACK_TO_LEARNING"