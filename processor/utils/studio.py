import numpy as np
import uuid
import json


def is_valid_class(class_name):
    if class_name == 'Part':
        return True
    if class_name == 'UnionOperation':
        return True
    return False


class Position(object):

    def __init__(self, point: np.array) -> None:
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def __repr__(self):
        return f'Position(x: {self.x}, y: {self.y}, z: {self.z})'

    def __str__(self):
        return f'Position(x: {self.x}, y: {self.y}, z: {self.z})'

    def to_vector(self):
        return np.array([self.x, self.y, self.z])

    def to_vector(self):
        return np.array([self.x, self.y, self.z])

    def to_vector(self):
        return np.array([self.x, self.y, self.z])


class Axis:

    def __init__(self, vector: np.array) -> None:
        self.x = vector[0]
        self.y = vector[1]
        self.z = vector[2]

    def __repr__(self):
        return f'Axis(x: {self.x}, y: {self.y}, z: {self.z})'

    def __str__(self):
        return f'Axis(x: {self.x}, y: {self.y}, z: {self.z})'

    def to_vector(self):
        return np.array([self.x, self.y, self.z])


class Camera(object):

    def __init__(
            self,
            position: Position = None, 
            lookat: Position = None, 
            orientation: Axis = None, 
            component_id: str = None, 
            ancestors: [int] = None,
            start_idx: int = None,
            end_idx: int = None) -> None:
        self.position = position
        self.lookat = lookat
        self.orientation = orientation
        self.component_id = component_id
        self.ancestors = ancestors
        self.start_idx = start_idx
        self.end_idx = end_idx

    def loads(self, lua_metadata):
        position = lua_metadata['position']
        self.position = Position(
            point=[position['x'], position['y'], position['z']])
        orientation = lua_metadata['rotation']['lookVector']
        self.orientation = Axis(
            vector=[orientation['x'], orientation['y'], orientation['z']])
        self.cluster_idx, self.camera_idx, self.symmetric_flag = [
            int(x) for x in lua_metadata['cameraId'][19:].split('_')]

    def __repr__(self):
        return f"Camera (posistion: {self.position}, orientation: {self.orientation}, camera_id: componentSnapshot-{self.component_id}, start_idx: {self.start_idx}, end_idx: {self.end_idx})"

    def __str__(self):
        return f"Camera (posistion: {self.position}, orientation: {self.orientation}, camera_id: componentSnapshot-{self.component_id}, start_idx: {self.start_idx}, end_idx: {self.end_idx})"

    def parse_to_proto(self):
        return {
            "camera_id": f'componentSnapshot-{self.component_id}',
            'position': {
                'x': self.position.x,
                'y': self.position.y,
                'z': self.position.z
            },
            'rotation': {
                'look_vector': {
                    'x': self.orientation.x,
                    'y': self.orientation.y,
                    'z': self.orientation.z
                }
            },
            'properties': json.dumps({'ancestor': self.ancestors, 'start': self.start_idx, 'end': self.end_idx})
        }

    def parse_to_lua(self):
        return {
            "cameraId": f'componentSnapshot-{self.component_id}',
            'position': {
                'x': self.position.x,
                'y': self.position.y,
                'z': self.position.z
            },
            'rotation': {
                'lookVector': {
                    'x': self.orientation.x,
                    'y': self.orientation.y,
                    'z': self.orientation.z
                }
            },
            'properties': json.dumps({'ancestor': self.ancestors, 'start': self.start_idx, 'end': self.end_idx})
        }
