from math import pi
import numpy as np

class Transform3D(object):
    
    def __init__(self) -> None:
        pass

    def transform(self, position, size, orientation):
        # point order top 1,2,3,4, bottom 1,2,3,4
        cube = np.array([
            [0.5,0.5,0.5,1], 
            [-0.5,0.5,0.5,1],
            [-0.5,-0.5,0.5,1], 
            [0.5,-0.5,0.5,1],
            [0.5,0.5,-0.5,1], 
            [-0.5,0.5,-0.5,1],
            [-0.5,-0.5,-0.5,1], 
            [0.5,-0.5,-0.5,1],
        ])

        cube = np.array([self.rotate(x, orientation) for x in cube])
        cube = np.array([self.scale(x, size) for x in cube])
        # cube = np.array([np.matmul(translation, x) self.translate(x, position) for x in cube])
        cube = np.array([self.translate(x, position) for x in cube])

        return cube
        
    def translate(self, point, position):
        # translate
        translation = np.array([
            [1, 0, 0, position['x']],
            [0, 1, 0, position['y']],
            [0, 0, 1, position['z']],
            [0, 0, 0, 1],
        ])

        return np.matmul(translation, point)
        
    def scale(self, point, size):
        # scale
        scale = np.array([
            [size['x'], 0, 0, 0],
            [0, size['y'], 0, 0],
            [0, 0, size['z'], 0],
            [0, 0, 0, 1],
        ])

        return np.matmul(scale, point)


    def rotate(self, point, orientation):
        # rotation
        rotation_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(orientation['x']), -np.sin(orientation['x']), 0],
            [0, np.sin(orientation['x']), np.cos(orientation['x']), 0],
            [0, 0, 0, 1],
        ])

        rotation_y = np.array([
            [np.cos(orientation['y']), 0, np.sin(orientation['y']), 0],
            [0, 1, 0, 0],
            [-np.sin(orientation['y']), 0, np.cos(orientation['y']), 0],
            [0, 0, 0, 1],
        ])

        rotation_z = np.array([
            [np.cos(orientation['z']), -np.sin(orientation['z']), 0, 0],
            [np.sin(orientation['z']), np.cos(orientation['z']), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

        return np.matmul(rotation_z, np.matmul(rotation_y, np.matmul(rotation_x, point)))


    def get_bounding_box(self, cube):
        return np.array([
            [min(cube[:, 0]), max(cube[:, 0])], 
            [min(cube[:, 1]), max(cube[:, 1])], 
            [min(cube[:, 2]), max(cube[:, 2])]
        ])


    def rodrigues_rotate(self, point, k, theta):
        k /= np.linalg.norm(k)

        I = np.identity(3)
        K = np.array([
            [0, -k[2], k[1]],
            [k[2], 0, -k[0]],
            [-k[1], k[0], 0]
        ])

        R = I + K * np.sin(theta) + np.matmul(K, K * (1 - np.cos(theta)))
        
        return np.matmul(point, R)

    def projection(self, v1, v2):
        return np.dot(v1, v2) / np.linalg.norm(v2)
    
    def unit_vector(self, vector):
        return vector / np.linalg.norm(vector)
    
    def angle_between(self, v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
