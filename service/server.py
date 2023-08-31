import grpc
from concurrent import futures
import service.proto.component_snapshot_pb2_grpc as pb2_grpc
import service.proto.component_snapshot_pb2 as pb2
from grpc_reflection.v1alpha import reflection

from processor import *

# from curses import meta
# from statistics import median

import logging, sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(fmt)
logger.addHandler(ch)

fh = logging.FileHandler('log/log', 'a', 'utf-8') 
fh.setFormatter(fmt) 
logger.addHandler(fh)


class ComponentSnapshotServicer(pb2_grpc.ComponentSnapshotServicer):

    def __init__(self, *args, **kwargs):
        pass
    
    def GetCameras(self, request, context):
        # get the string from the incoming request
        logger.info(f'Receive request for Asset ID: {request.asset_id} - Version: {request.version} - Asset type: {request.asset_type} - Snapshot ID: {request.snapshot_id}')
        logger.info(f'Start component snapshot...')
        
        processor = Processor(
            metadata=request.raw_metadata, 
            depth=1)
        processor.transform()

        cameras = [c.parse_to_proto() for c in processor.cameras]
        logger.info(f'Finished component snapshot.')

        result = {
            'metadata': {'cameras': pb2.Metadata(**{'object_metadata': cameras})}
        }
        
        if not cameras:
            result = {}
            logger.info(f'No component found...')

        return pb2.RccOutput(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options = [
        ('grpc.max_send_message_length', 200 * 1024 * 1024 * 8),
        ('grpc.max_receive_message_length', 200 * 1024 * 1024 * 8)
    ])
    
    pb2_grpc.add_ComponentSnapshotServicer_to_server(ComponentSnapshotServicer(), server)
    SERVICE_NAMES = (
        pb2.DESCRIPTOR.services_by_name['ComponentSnapshot'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logger.info(f'Initialized gRPC server for component snapshot on port 50052.')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()