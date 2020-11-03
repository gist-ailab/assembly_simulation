from pyrep.objects.object import Object
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
from pyrep.objects.vision_sensor import VisionSensor

from enum import Enum
from os import path
from typing import List
from pyquaternion import Quaternion
import numpy as np

class Camera():
    def __init__(self, name, resolution, perspective_angle, min_depth, max_depth, near_clipping=0.2, far_clipping=3):
        self.base = Dummy(name)
        self.cam_rgb = VisionSensor(name + "_rgb")
        self.cam_depth = VisionSensor(name + "_depth")
        self.cam_mask = VisionSensor(name + "_mask")
        self.cam_all = [self.cam_rgb, self.cam_depth, self.cam_mask]
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.set_resolution(resolution)
        self.set_perspective_angle(perspective_angle)
        self.set_near_clipping_plane(near_clipping)
        self.set_far_clipping_plane(far_clipping)

    def get_resolution(self):
        return self._resolution
    def set_resolution(self, resolution):
        for cam in self.cam_all:
            cam.set_resolution(resolution)
        self._resolution = resolution
    
    def get_perspective_angle(self):
        return self._perspective_angle
    def set_perspective_angle(self, angle: float):
        for cam in self.cam_all:
            cam.set_perspective_angle(angle)
        self._perspective_angle = angle

    def set_near_clipping_plane(self, near_clipping):
        self.cam_rgb.set_near_clipping_plane(near_clipping)
        self.cam_mask.set_near_clipping_plane(near_clipping)
        self.cam_depth.set_near_clipping_plane(self.min_depth)
    def set_far_clipping_plane(self, far_clipping):
        self.cam_rgb.set_far_clipping_plane(far_clipping)
        self.cam_mask.set_far_clipping_plane(far_clipping)
        self.cam_depth.set_far_clipping_plane(self.max_depth)

    def capture_rgb(self):
        return np.uint8(255*self.cam_rgb.capture_rgb())[:, :, ::-1]
    def capture_depth(self):
        return np.uint8(255*self.cam_depth.capture_depth())
    def capture_mask(self):
        mask = np.uint8(255*self.cam_mask.capture_rgb())
        mask = mask[:, :, 1]
        mask[mask!=0] = 1
        return mask

    def set_pose(self, pose, relative_to=None):
        pos = pose[:3]
        qx, qy, qz, qw = pose[3:]
        quat_ori = Quaternion([qw, qx, qy, qz])
        quat_rotate_z = Quaternion(axis=[0, 0, 1], angle=np.radians(180))
        quat = quat_ori*quat_rotate_z
        qw, qx, qy, qz = quat.elements
        quat = [qx, qy, qz, qw]
        # quat = pose[3:]
        self.base.set_pose([*pos] + [*quat], relative_to=relative_to)

    def get_image(self):
        rgb = self.capture_rgb()
        depth = self.capture_depth()
        mask = self.capture_mask()
        return rgb, depth, mask

class Object_():
    def __init__(self, name):
        
        self.obj_frame = Dummy(name + '_frame')
        self.obj_visible = Shape(name + '_visible')
        self.obj_respondable = Shape(name + '_respondable')
        self.obj_mask = Shape(name + '_mask')

    #region transform -> self.obj_frame
    def get_pose(self, relative_to=None):
        self.obj_frame.get_pose(relative_to=relative_to)    
    
    def set_pose(self, pose, relative_to=None):
        """
        :param pose: An array containing the (X,Y,Z,Qx,Qy,Qz,Qw) pose of
            the object.
        """
        self.obj_frame.set_parent(None)
        self.obj_respondable.set_parent(self.obj_frame)
        # self.obj_visible.set_parent(self.obj_respondable)
        self.obj_frame.set_pose(pose, relative_to=relative_to)
        self.obj_respondable.set_parent(None)
        self.obj_frame.set_parent(self.obj_respondable)
        # self.obj_visible.set_parent(self.obj_respondable)
        
    
    #endregion

    #region physics and shape property -> self.shape
    def is_dynamic(self):
        return self.shape.is_dynamic()
    def set_dynamic(self, value: bool):
        self.shape.set_dynamic(value)
    
    def is_respondable(self):
        return self.shape.is_respondable()
    def set_respondable(self, value: bool):
        self.shape.set_respondable(value)
    
    def is_collidable(self):
        return self.shape.is_collidable()
    def set_collidable(self, value: bool):
        self.shape.set_collidable(value)
    
    def is_detectable(self):
        return self.shape.is_detectable()
    def set_detectable(self, value: bool):
        self.shape.set_detectable(value)
    
    def is_renderable(self):
        return self.shape.is_renderable()
    def set_renderable(self, value: bool):
        self.shape.set_renderable(value)

    def check_collision(self, obj=None):
        return self.shape.check_collision(obj)    

    #endregion
    def remove(self):
        self.shape.remove()
        self.obj_frame.remove()


