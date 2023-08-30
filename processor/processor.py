
from processor.utils.transform3d import Transform3D
import processor.utils.studio as RBX
from sklearn.decomposition import PCA

import numpy as np
from math import pi
from collections import Counter

import json

import logging
import sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 
fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(fmt)
logger.addHandler(ch)

# fh = logging.FileHandler('logs/log', 'a', 'utf-8') 
# fh.setFormatter(fmt) 
# logger.addHandler(fh)

class ModelComponentProcessor(object):

    CAMERA_FOV = 70
    CAMERA_DISTANCE_FACTOR = 3
    MIN_NUMBER_OF_OBJECT_IN_COMPONENT = 5

    def __init__(
        self, 
        metadata,
        depth
    ) -> None:
        self.model = self._load(metadata)
        self.depth = depth
        self.t3d: Transform3D = Transform3D()

    def _load(self, metadata):
        model = json.loads(metadata)['outputAllDescendent']['info']
        return model

    def _build_component(self):
        self._make_depth()
        self.components = [([], 0, len(self.model))]
        
        layer1 = [i for i, x in enumerate(self.depth) if x == 2] + [len(self.model)]
        for i in range(len(layer1) - 1):
            self.components.append(([0], layer1[i], layer1[i+1]))

        layer2 = [i for i, x in enumerate(self.depth) if x == 3] + [len(self.model)]
        parent = 0
        for i in range(len(layer2) - 1):
            st, ed = layer2[i], layer2[i+1]
            if st > layer1[parent + 1]:
                parent += 1
            if ed > layer1[parent + 1]:
                ed = layer1[parent + 1]
            self.components.append(([0, layer1[parent]], st, ed))
        
        self._dedupe_components()

    def _make_depth(self):
        path = ['ContainerModel']

        self.depth = []
        for i, object in enumerate(self.model):
            while '.'.join(path) + '.' + object['name'] != object['fullPath']:
                path.pop()
            self.depth.append(len(path))
            path.append(object['name'])

    def _dedupe_components(self):
        self.components = [x for x in self.components if x[2] - x[1] > self.MIN_NUMBER_OF_OBJECT_IN_COMPONENT]
        result = []
        for component in self.components:
            ancestors, start, end = component
            if end - start  < self.MIN_NUMBER_OF_OBJECT_IN_COMPONENT:
                continue
            if all(['size' not in x for x in self.model[start:end]]):
                continue
            result.append((component))
        self.components = result
            
    def _pca(self, X) -> np.array:
        pcs = []
        # for i in range(3):
        #     if len(set(X[:, i])) <= 1:
        #         vec = np.zeros(3)
        #         vec[i] = 1.0
        #         pcs.append(vec)
        
        # if len(X) + len(pcs) < 3:
        #     pcs.append(np.array([1.0, 0, 0]))
        #     pcs.append(np.array([0, 1.0, 0]))
        #     pcs.append(np.array([0, 0, 1.0]))
        # elif len(pcs) < 3: 
        #     pca = PCA(n_components=3 - len(pcs))
        #     pca.fit_transform(X)
        #     for pc in pca.components_[np.argsort(pca.explained_variance_)]:
        #         if self.t3d.projection(pc, np.array([0, -1, 0])) < 0:
        #             pcs.append(-pc)
        #         elif self.t3d.projection(pc, np.array([0, 0, -1])) < 0:
        #             pcs.append(-pc)
        #         elif self.t3d.projection(pc, np.array([-1, 0, 0])) < 0:
        #             pcs.append(-pc)
        #         else:
        #             pcs.append(pc)

        pcs.append(np.array([0, 0, 1.0]))
        pcs.append(np.array([1.0, 0, 0]))
        pcs.append(np.array([0, 1.0, 0]))

        return np.array(pcs)

    def _get_objects_for(self, component):
        objects = []
        for ancestor in component[0]:
            objects.append(self.model[ancestor])
        st, ed =  component[1:]
        objects += self.model[st:ed]
        return objects

    def _compute_camera(self):
        self.cameras = []
        for component in self.components:
            objects = self._get_objects_for(component)
            try:
                points = self._extract_object_points(objects)
                pcs = self._pca(X=points)

                ranges, center = self._compute_ranges_and_center(points, pcs)

                shift = self._compute_camera_shift(ranges[1], ranges[2], ranges[0])
                self.cameras.append(self._generate_camera(center, pcs[0], shift, component))
                logger.info(f'compute_camera: SUCCEEDED for component #{component}.')
            except:
                logger.warning(f'compute_camera: FAILED to compute camera for component #{component}.')

    
    def _compute_camera_shift(self, axis_x, axis_y, axis_z):
        tan = np.tan(np.radians(self.CAMERA_FOV / 2))
        delta_x = tan * axis_x / 2
        delta_y = tan * axis_y / 2
        delta_z = axis_z / 2

        return np.max([delta_x, delta_y, delta_z])

    def _generate_camera(
            self, 
            lookat_position, 
            lookup_vector, 
            shift, 
            component):
        nodes = []
        ancestors, start_idx, end_idx = component
        
        for ancestor in ancestors:
            nodes.append(self.model[ancestor]['name'])
        nodes.append(self.model[component[1]]['name'])

        return RBX.Camera(
            position=RBX.Position(lookat_position - shift * lookup_vector * self.CAMERA_DISTANCE_FACTOR),
            lookat=lookat_position,
            orientation=RBX.Axis(lookup_vector),
            component_id='.'.join(nodes),
            ancestors=ancestors,
            start_idx=start_idx,
            end_idx=end_idx
        )

    def _compute_ranges_and_center(self, points, components): 
        ranges, medians = [], np.array([])
        component = np.array
        for component in components: 
            projections = np.array([self.t3d.projection(p, component) for p in points])
            ranges.append(projections.max() - projections.min())
            medians = np.append(medians, ((projections.max() + projections.min()) / 2))

        return ranges, np.dot(medians, components)

    def _extract_object_points(self, objects):
        points = np.array([])
        for obj in objects:
            if 'size' not in obj: continue
            if 'position' not in obj: continue
            if 'orientation' not in obj: continue
            cube = self.t3d.transform(obj['position'], obj['size'], obj['orientation'])
            points = np.append(points, cube[:, :3])

        points = points.reshape(int(points.shape[0] / 3), 3)

        return points


    def transform(self):
        self._build_component()
        self._compute_camera()