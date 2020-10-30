from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy

from pyrep.objects.vision_sensor import VisionSensor

from enum import Enum
from os import path
from typing import List

class Camera():
    def __init__(self, sensor: VisionSensor):
        self.sensor = sensor

    @staticmethod
    def create(resolution: List[int], near_clipping_plane=1e-2, far_clipping_plane=10.0, view_angle=60.0):
        sensor = VisionSensor.create(resolution=resolution,
                                     near_clipping_plane=near_clipping_plane,
                                     far_clipping_plane=far_clipping_plane,
                                     view_angle=view_angle)
        
        return Camera(sensor)

    def get_resolution(self):
        self.sensor.get_resolution()
    def set_resolution(self, resolution):
        self.sensor.set_resolution(resolution)
    
    def get_perspective_angle(self):
        self.sensor.get_perspective_angle()
    def set_perspective_angle(self, angle: float):
        self.sensor.set_perspective_angle(angle)

    def capture_rgb(self):
        self.sensor.capture_rgb()
    def capture_depth(self):
        self.sensor.capture_depth()

    def set_pose(self, pose, relative_to=None):
        self.sensor.set_pose(pose, relative_to=relative_to)

    def get_image(self):
        rgb = self.capture_rgb()
        depth = self.capture_depth()
        
        return rgb, depth

class ObjObject():
    def __init__(self, obj: Shape):
        self.shape = obj
        self.name = self.shape.get_name()
        try:
            self.frame = Dummy(self.name + "_frame")
        except:
            print("{} object is not ObjObject".format(self.name))
            exit()

    @staticmethod
    def create_object(obj_path, scaling_factor=1):
        file_name, ext = path.splitext(obj_path)
        obj_name = file_name.split("/")[-1]
        if not ext == ".obj":
            print("[ERROR] please check obj file {}".format(obj_path))
            exit()
        obj = Shape.import_mesh(obj_path, scaling_factor=scaling_factor)
        obj.set_name(obj_name)
        obj_base = Dummy.create()
        obj_base.set_name(obj_name + "_frame")

        obj_base.set_parent(obj)

        return ObjObject(obj)

    #region transform -> self.frame
    def get_pose(self, relative_to=None):
        self.frame.get_pose(relative_to=relative_to)    
    
    def set_pose(self, pose, relative_to=None):
        """
        :param pose: An array containing the (X,Y,Z,Qx,Qy,Qz,Qw) pose of
            the object.
        """
        self.frame.set_parent(None)
        self.shape.set_parent(self.frame)
        self.frame.set_pose(pose, relative_to=relative_to)
        self.shape.set_parent(None)
        self.frame.set_parent(self.shape)
        
    
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
        self.frame.remove()


