import grpc
import service.proto.component_snapshot_pb2_grpc as pb2_grpc
import service.proto.component_snapshot_pb2 as pb2
import argparse


class ComponentSnapshotClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self, port=50051):
        self.host = 'localhost'
        self.server_port = port

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.ComponentSnapshotStub(self.channel)

    def get_url(self, metadata, asset_id, version, asset_type, snapshot_id):
        """
        Client function to call the rpc for GetServerResponse
        """
        request = pb2.GetCamerasRequest(
            raw_metadata=metadata,
            asset_id=asset_id,
            version=version,
            asset_type=asset_type,
            snapshot_id=snapshot_id
        )
        return self.stub.GetCameras(request)


if __name__ == '__main__':

    argParser = argparse.ArgumentParser()
    argParser.add_argument('metadata', type=argparse.FileType('r'))
    argParser.add_argument("-a", "--asset_id", required=False, type=str, help="Input Asset ID.")
    argParser.add_argument("-v", "--version", required=False, type=str, help="Input Asset Version.")
    argParser.add_argument("-t", "--asset_type", required=False, type=str, help="Input Asset Type.")
    argParser.add_argument("-s", "--snapshot_id", required=False, type=str, help="Input Snapshot ID.")
    argParser.add_argument("-p", "--port", required=False, type=int, help="Server Port.")
    args = argParser.parse_args()
    port = args.port
    if not port: port = 50051
    client = ComponentSnapshotClient(port)
    metadata = args.metadata.read()
    # snap = '9159465565-806395725244989499'
    # print('111',metadata)
    # with open(f'data/{snap}.json', 'r') as f:
    #     metadata = f.read()
    result = client.get_url(
        metadata=metadata,
        asset_id=args.asset_id,
        version=args.version,
        asset_type=args.asset_type,
        snapshot_id=args.snapshot_id
    )
    print(result)
    print(str(result))
