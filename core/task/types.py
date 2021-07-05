from enum import Enum, auto

class TaskType(Enum):
    RUN_EXECUTABLE = auto()

class ResultStatus(Enum):
    PENDING = auto()
    SUCCESS = auto()
    OUTPUT_MISMATCH = auto()
    RUNTIME_ERR = auto()
    INF_LOOP = auto()
    FILE_NOT_FOUND = auto()
