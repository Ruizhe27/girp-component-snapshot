import json
import requests

from .enums import *
from .config import GIRPConfig
import numpy as np

class GIRPProcessor(object):
    def __init__(self, config: GIRPConfig) -> None:
        self.config = config

        if config.env == Environment.PROD:
            self._girp_snapshot_url = "https://apis.roblox.com/game-snapshots/v1/GetSnapshotsForPlace"
            self._api_key = "5306596e-2d39-42e5-98bd-3436be2ddc1f"
        elif config.env == Environment.ST3:
            self._girp_snapshot_url = "https://apis.sitetest3.robloxlabs.com/game-snapshots/v1/GetSnapshotsForPlace"
            self._api_key = "0ebca04a-4ab3-4a24-afb7-19b0775eb57a"

        self.headers = {"Roblox-Api-Key": self._api_key}

    def place_info_gather(self, asset_id, version):
        self.asset_id = asset_id
        self.version = version

        body = {
            "placeId": asset_id,
            "placeVersion": version,
            "snapshotFormat": self.config.snapshotFormat,
            "metadataCommandType": self.config.metadataCommandType,
            "SqsQueue": self.config.SqsQueue,
            "overrideHistory": self.config.overrideHistory
        }

        resp = requests.post(self._girp_snapshot_url,
                             json=body,
                             headers={"Roblox-Api-Key": self._api_key})
        self.snap = json.loads(resp.text)['placeSnapshotId']

        return self.snap
   

    def cluster_video(self, asset_id, version):

        self.asset_id = asset_id
        self.version = version

        body = {
            "placeId": asset_id,
            "placeVersion": version,
            "snapshotFormat": self.config.snapshotFormat,
            "metadataCommandType": self.config.metadataCommandType,
            "SnapshotCommandType": self.config.SnapshotCommandType,
            "SqsQueue": self.config.SqsQueue,
            "overrideHistory": self.config.overrideHistory
        }

        resp = requests.post(self._girp_snapshot_url,
                             json=body,
                             headers={"Roblox-Api-Key": self._api_key})
        self.snap = json.loads(resp.text)['placeSnapshotId']

        return self.snap
            
    def _create_video_job(self, asset_id, version, cameras):
        job = dict()

        job['MessageVersion'] = 1
        job['Mode'] = 'ExecuteScript'
        settings = dict()
        settings['Type'] = 'ClustersVideo'
        arguments = dict()
        arguments =  [
            "http://www.s.robloxdev.cn",
            f"https://s.robloxdev.cn/asset?id={asset_id}&version={version}",
            "1024",
            "1024",
            cameras]
        settings['Arguments'] = arguments
        job['Settings'] = settings
        job['MessageVersion'] = 1

        return job

    def generate_video_batch_job(self, asset_id, version, cameras, batch_size=5):
        jobs = []

        for i in range(int(np.ceil(len(cameras) / batch_size))):
            st, ed = max(0, i * batch_size - 1),(i + 1) * batch_size
            job = self._create_video_job(asset_id, version, cameras[st:ed])
            jobs.append(job)

        return jobs
