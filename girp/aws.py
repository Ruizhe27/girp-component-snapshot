from pathlib import Path
import json

import boto3
from .enums import *
from .config import GIRPConfig
from numpy import ceil
import shutil
# from moviepy.editor import VideoFileClip, concatenate_videoclips


class AWSProcessor(object):

    def __init__(self, config: GIRPConfig) -> None:
        self.config = config
        self.bucket_name = ''

    def download_metadata_from_s3(self, snap, save_folder: Path):
        s3 = boto3.client('s3')
        if self.config.env == Environment.PROD:
            bucket_name = 'place-snapshot-json'
        elif self.config.env == Environment.ST3:
            bucket_name = 'place-snapshot-json-test'
        else:
            print('download_metadata: Environment is not PROD nor ST3. Terminated.')
            return

        if not save_folder.is_dir():
            save_folder.mkdir()

        metadata_name = 'metadata.json'
        if self.config.command in [CommandType.CLUSTER_VIDEO_FOR_PLACE, CommandType.COMPONENT_SNAPSHOT] :
            metadata_name = 'cameras.json'
        if not (save_folder/metadata_name).is_file():
            # try:
            s3.download_file(
                bucket_name, f'{snap}.json', str(save_folder/metadata_name))
            print(f'download_metadata: Succeeded to download {snap}.json')
            # except:
            #     shutil.rmtree(save_folder)
            #     print(f'download_metadata: Failed to download {snap}.json')

    def download_snapshots_from_s3(self, snap, save_folder: Path):
        s3_resource = boto3.resource('s3')
        if self.config.env == Environment.PROD:
            bucket_name = 'place-snapshot-items'
        elif self.config.env == Environment.ST3:
            bucket_name = 'place-snapshot-items-test'
        else:
            print('Environment is not PROD nor ST3. Terminated.')
            return

        bucket = s3_resource.Bucket(bucket_name)

        if not save_folder.is_dir():
            save_folder.mkdir()

        for obj in bucket.objects.filter(Prefix=str(snap)):
            # TODO: using pathlib
            pass
            # key = os.path.dirname(obj.key).split('/')[-1]
            # if not os.path.exists(f'{folder}/{key}-{os.path.basename(obj.key)}'):
            #     bucket.download_file(obj.key, f'{folder}/{key}-{os.path.basename(obj.key)}')
            #     print(f'Downloaded {folder}/{key}-{os.path.basename(obj.key)}')



    def download_components(self, snap, save_folder: Path):
        s3_resource = boto3.resource('s3')
        if self.config.env == Environment.PROD:
            bucket_name = 'place-snapshot-items'
        elif self.config.env == Environment.ST3:
            bucket_name = 'place-snapshot-items-test'
        bucket = s3_resource.Bucket(bucket_name)

        if not save_folder.exists(): save_folder.mkdir()
        component_save_folder = save_folder / 'components'
        if not component_save_folder.exists(): component_save_folder.mkdir()

        count = 0
        for obj in bucket.objects.filter(Prefix=str(snap)):
            count += 1
            file_name = obj.key.split('componentSnapshot-')[-1].split('|<=*=>|')[-1]
            file_name = file_name.replace("/", ".")
            image_path = component_save_folder / file_name
                
            if not image_path.is_file():
                try:
                    bucket.download_file(obj.key, str(image_path))
                    print(f'download_component: snapshot {obj.key} downloaded')
                except:
                    print(f'download_component: Failed to download {obj.key}')
            else:
                print(f'download_component: snapshot {obj.key} already downloaded')
        print(f'download_component: {count} snapshots completed')


    def download_videos_from_s3(self, snap, save_folder:Path, merge_video: bool = True):
        if self.config.env == Environment.PROD:
            bucket_name = 'place-snapshot-items'
        elif self.config.env == Environment.ST3:
            bucket_name = 'place-snapshot-items-test'
        else:
            print('download_video: Environment is not PROD nor ST3. Terminated.')
            return

        if not save_folder.is_dir():
            save_folder.mkdir()

        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)

        count = 0
        for obj in bucket.objects.filter(Prefix=str(snap)):
            count += 1
            clip_path = save_folder / \
                f'{Path(obj.key).name[:-5].split("_")[-1]}.webm'
            if not clip_path.is_file():
                try:
                    bucket.download_file(obj.key, str(clip_path))
                    print(f'download_video: Clip {obj.key} downloaded')
                except:
                    print(f'download_video: Failed to download {obj.key}')
            else:
                print(f'download_video: Clip {obj.key} already downloaded')
        print(f'download_video: {count} clips completed')

    # def _merge_clips(self, save_folder: Path):
    #     videos = dict()
    #     sorted_videos = []

    #     for obj in save_folder.glob('*.webm'):
    #         videos[int(obj.parts[-1].split('.')[0])] = VideoFileClip(str(obj))
    #         sorted_videos = sorted(videos.items())
    #         sorted_videos = [x[1] for x in sorted_videos]

    #     final_video = concatenate_videoclips(sorted_videos)
    #     final_video.write_videofile(str(save_folder / "video.mp4"), threads=8)

    #     print('merge_clips: done.')



    