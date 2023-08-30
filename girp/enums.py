from enum import Enum


class CommandType(Enum):
    CLUSTER_VIDEO_FOR_PLACE = 0
    SNAPSHOT_FOR_PLACE = 1
    PLACE_INFO_GATHERER = 2
    MODEL_INFO_GATHERER = 3


class Environment(Enum):
    PROD = 0
    ST3 = 1
