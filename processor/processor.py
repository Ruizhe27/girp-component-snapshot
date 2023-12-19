
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
    MAX_NUM_OF_COMPONENTS = 50

    def __init__(
        self, 
        metadata,
        depth
    ) -> None:
        self.model = self._load(metadata)
        self.depth = depth
        self.t3d: Transform3D = Transform3D()
        self.keys = dict()

    def _load(self, metadata):
        model = json.loads(metadata)['outputAllDescendent']['info']
        return model

    def _build_component(self):
        self._make_depth()
        self.components = [([], 0, len(self.model))]
        
        layer1 = [i for i, x in enumerate(self.depth) if x == 2] + [len(self.model)]
        layer1_imgs = [x for x in self.images if self.depth[x] == 2] 
        img_idx = 0
        for i in range(len(layer1) - 1):
            self.components.append(([0], layer1[i], layer1[i+1]))

            if img_idx == len(layer1_imgs): continue
            next_image = layer1_imgs[img_idx]
            if next_image == layer1[i] and layer1[i+1] - layer1[i] > 1:
                self.components.append(([0], next_image, next_image + 1))
                img_idx += 1

        layer2 = [i for i, x in enumerate(self.depth) if x == 3] + [len(self.model)]
        layer2_imgs = [x for x in self.images if self.depth[x] > 2] 
        img_idx = 0
        parent = 0
        for i in range(len(layer2) - 1):
            st, ed = layer2[i], layer2[i+1]

            if st > layer1[parent + 1]:
                parent += 1
            while ed > layer1[parent + 1]:
                self.components.append(([0, layer1[parent]], st, layer1[parent + 1]))
                parent += 1
                st = layer1[parent + 1]
            if ed > st:
                self.components.append(([0, layer1[parent]], st, ed))

            while img_idx < len(layer2_imgs) and layer2_imgs[img_idx] >= st and layer2_imgs[img_idx] < ed:
                if not (ed - st == 1 and st == layer2_imgs[img_idx]):
                    self.components.append(([0, layer1[parent]], layer2_imgs[img_idx], layer2_imgs[img_idx] + 1))
                img_idx += 1

        self._dedupe_components()

    def _make_depth(self):
        path = ['Workspace.ContainerModel']

        self.depth = []
        self.images = []
        images_URLs = set()
        for i, object in enumerate(self.model):
            if 'imageUrl' in object:
                url = object['imageUrl']
                if self._is_image_URL(url) and url not in images_URLs:
                    self.images.append(i)
                    images_URLs.add(url)

            while '.'.join(path) + '.' + object['name'] != object['fullPath']:
                path.pop()
            self.depth.append(len(path))
            path.append(object['name'])

    def _dedupe_components(self):
        logger.info(f'dedupe_components: start to dedupe components.')
        result = []
        for i, component in enumerate(self.components):
            if len(result) >= self.MAX_NUM_OF_COMPONENTS: 
                logger.info(f'dedupe_components: STOPPED. Exceeds the max number of components.')
                break
            _, start, end = component
            name = self.model[start]['name']
            if self._is_screen_GUI(component): 
                result.append(component)
                logger.info(f'dedupe_components: component #{component}-{name} is a Screen GUI.')
                continue
            if end - start == 1 and start in self.images: 
                result.append(component)
                logger.info(f'dedupe_components: component #{component}-{name} is an Image.')
                continue
            if all(['size' not in x for x in self.model[start:end]]): 
                logger.info(f'dedupe_components: component #{component}-{name} deduped, no physical objects.')
                continue
            if all([x['transparency'] == 1 for x in self.model[start:end] if 'transparency' in x]):
                logger.info(f'dedupe_components: component #{component}-{name} deduped, transparent component.')
                continue
            if name not in self.keys:
                self.keys[name] = [i]
                result.append(component)
                continue

            is_duplicate = False
            for key in self.keys[name]:
                if self._is_duplicate(self.components[key], component):
                    is_duplicate = True
                    logger.info(f'dedupe_components: component #{component}-{name} deduped, duplicate to #{key}.')
                    break
            
            if not is_duplicate: 
                self.keys[name].append(i)
                result.append((component))
        self.components = result
    
    def _is_duplicate(self, key, comp):
        key_objects = self._get_objects_for(key)
        comp_objects = self._get_objects_for(comp)


        key_meshes = set([y for x in key_objects for y in x.values() if type(y) == str and '://' in y])
        comp_meshes = set([y for x in comp_objects for y in x.values() if type(y) == str and '://' in y])
        if key_meshes and comp_meshes:
            return key_meshes == comp_meshes
        else:
            key_names = set([x['name'] for x in key_objects])
            comp_names = set([x['name'] for x in comp_objects])
            if key_names == comp_names: return True

        return False

    def _pca(self, X: np.array) -> np.array:
        # x_sd = self._compute_standard_deviation(X, np.array(1, 0, 0))
        # z_sd = self._compute_standard_deviation(X, np.array(0, 0, 1))
        x_sd = np.std(np.array([self.t3d.projection(p, np.array([1, 0, 0])) for p in X]))
        z_sd = np.std(np.array([self.t3d.projection(p, np.array([0, 0, 1])) for p in X]))
        logger.info(f'pca: sd for x axis is {x_sd}, sd for z axis is {z_sd}')
        pcs = np.array([
            [0, 0, 1],
            [0, 1, 0],
            [1, 0, 0]
        ])

        if x_sd > z_sd:
            logger.info(f'pca: projection along x axis got higher sd, change camera orientation to z-axis')
            pcs = np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ])
        return pcs
        # if X.shape[0] < 3:
        #     X = np.repeat(X, repeats=3, axis=0)
        
        # pca = PCA(n_components=3)
        # pca.fit_transform(X)

        # return pca.components_

    def _get_objects_for(self, component):
        st, ed =  component[1:]
        return self.model[st:ed]
    
    def _is_screen_GUI(self, component):
        _, start, _ = component
        return 'isScreenGui' in self.model[start]

    def _is_image_URL(self, image_URL):
        return 'rbxassetid://' in image_URL or 'http://www.roblox.com/asset/?id=' in image_URL
    
    def _compute_camera(self):
        self.cameras = []
        for component in self.components:
            try:
                if self._is_screen_GUI(component): 
                    self.cameras.append(self._generate_camera(
                        np.array([0, 0, 0]), 
                        np.array([0, 0, 0]), 
                        0, 
                        component, 
                        'GUI'))
                elif component[2] - component[1] == 1 and component[1] in self.images:
                    self.cameras.append(self._generate_camera(
                        np.array([0, 0, 0]), 
                        np.array([0, 0, 0]), 
                        0, 
                        component, 
                        'IMAGE', 
                        self.model[component[1]]['imageUrl']))
                else:
                    objects = self._get_objects_for(component)
                    points = self._extract_object_points(objects)
                    if points.shape[0] == 0:
                        logger.info(f'compute_camera: FAILED for component #{component}, no valid objects.')
                        continue

                    pcs = self._pca(X=points)

                    ranges, center = self._compute_ranges_and_center(points, pcs)

                    shift = self._compute_camera_shift(ranges[0], ranges[1], ranges[2])
                    self.cameras.append(self._generate_camera(center, pcs[2], shift, component))
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
            component, 
            type='MODEL',
            url=None,):
        nodes = []
        ancestors, start_idx, end_idx = component
        
        for ancestor in ancestors:
            nodes.append(f'{self.model[ancestor]["name"]}{ancestor}')
        nodes.append(f"{self.model[component[1]]['name']}{component[1]}")

        return RBX.Camera(
            position=RBX.Position(lookat_position - shift * lookup_vector * self.CAMERA_DISTANCE_FACTOR),
            lookat=lookat_position,
            orientation=RBX.Axis(lookup_vector),
            component_id='|<=*=>|'.join(nodes),
            ancestors=ancestors,
            start_idx=start_idx,
            end_idx=end_idx,
            url=url,
            component_type=type
        )

    def _compute_standard_deviation(self, points, component):
        projections = np.array([self.t3d.projection(p, component) for p in points])
        return np.std(projections)

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
            if obj['className'] == 'Model': continue
            if 'transparency' in obj and obj['transparency'] == 1: continue
            cube = self.t3d.transform(obj['position'], obj['size'], obj['orientation'])
            points = np.append(points, cube[:, :3])

        points = points.reshape(int(points.shape[0] / 3), 3)
        return points


    def transform(self):
        self._build_component()
        self._compute_camera()