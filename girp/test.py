from config import Config
from enums import CommandType, Environment

config = Config(command=CommandType.CLUSTER_VIDEO_FOR_PLACE,
                env=Environment.PROD)
print(config.command)
print(config.metadataCommandType)
