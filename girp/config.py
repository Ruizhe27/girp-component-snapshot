from .enums import *


class GIRPConfig(object):
    snapshotFormat = 'PNG1024x1024'
    overrideHistory = True
    metadataCommandType = None
    SnapshotCommandType = None
    # SqsQueue = None

    def __init__(self, command: CommandType, env: Environment) -> None:
        self.command = command
        self.env = env

        if self.command == CommandType.PLACE_INFO_GATHERER:
            self.metadataCommandType = 'PlaceInfoGatherer'
        if self.command == CommandType.MODEL_INFO_GATHERER:
            self.metadataCommandType = 'ModelInfoGatherer'
        elif self.command == CommandType.CLUSTER_VIDEO_FOR_PLACE:
            self.metadataCommandType = 'PlaceInfoGatherer'
            self.SnapshotCommandType = 'ClustersVideoForPlace'
        elif self.command == CommandType.COMPONENT_SNAPSHOT:
            self.metadataCommandType = 'ModelInfoGatherer'
            self.SnapshotCommandType = 'ComponentSnapshot'

        if self.env == Environment.PROD:
            self.SqsQueue = 'placeSnapshotWorkItemQueue'

            if self.command == CommandType.COMPONENT_SNAPSHOT:
                self.SqsQueue = 'placeSnapshotWorkItemQueue'
