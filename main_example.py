from pyrep import PyRep
from os import path

from pyrep.objects import Shape
from pyrep.objects import Dummy
from scene_object import Camera, ObjObject

if __name__ =="__main__":
    scene_file = "./assembly_env.ttt"
    pr = PyRep()
    pr.launch(scene_file=scene_file, headless=False)
    pr.start()
    
    world_base = Dummy("world_frame")

    obj_path = "./ikea_stefan_long.obj"
    obj1 = ObjObject.create_object(obj_path=obj_path, scaling_factor=0.001)
    pr.step()
    
    cam1 = Camera.create([1280, 720])
    cam1.set_pose([0, 0, 0, 0, 0, 0, 1], relative_to=world_base)

    for i in range(100):
        obj1.set_pose([i/100, 0, 0, 0, 0, 0, 1], relative_to=world_base)
        rgb, depth = cam1.get_image()
        pr.step()

    pr.export_scene("test.ttt")
    
    pr.stop()
    pr.shutdown()
