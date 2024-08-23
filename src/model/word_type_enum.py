import enum

class WordTypeEnum(str, enum.Enum):
    standard = "STANDARD"
    custom = "CUSTOM"
    test = "TEST_WORD_TYPE"
