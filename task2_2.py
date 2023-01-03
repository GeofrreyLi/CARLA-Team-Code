import glob
import os
import sys
import time


try:
    sys.path.append(glob.glob('../../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt

_HOST_ = '127.0.0.1'
_PORT_ = 2000
_SLEEP_TIME_ = 1
IM_WIDTH = 800
IM_HEIGHT = 600

def process_img(image, str):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow(str, i3)
    cv2.waitKey(1)
    # cc = carla.ColorConverter.LogarithmicDepth
    image.save_to_disk('_out/%06d.png' % image.frame)
    return i3 / 255.0

actors = []

client = carla.Client('localhost', 2000)  # https://carla.readthedocs.io/en/0.9.11/core_world/#the-client
client.set_timeout(10.0)

world = client.get_world()
blueprint_library = world.get_blueprint_library()

# get pedestrian, rgb camara, and walker
walker_controller_bp = blueprint_library.find('controller.ai.walker')
walker_bp = blueprint_library.filter("walker.pedestrian.*")
sensor = blueprint_library.find('sensor.camera.rgb')
# get location of the world
trans = carla.Transform()
trans.location = world.get_random_location_from_navigation()
trans.location.z += 1
# spawn walker
walker = random.choice(walker_bp)
actor = world.spawn_actor(walker, trans)
world.wait_for_tick()
# spawn controller
controller = world.spawn_actor(walker_controller_bp, carla.Transform(), actor)
world.wait_for_tick()
# spawn rgb camara to the pedestrian
spawn_point_walker = carla.Transform(carla.Location(x=0.6, y=-0.45, z=1.6))
actor_sensor = world.spawn_actor(blueprint=sensor, transform=spawn_point_walker,
                                 attach_to=actor)
# register listener for rgb camara
actor_sensor.listen(lambda data: process_img(data, "sensor2"))


actors.append(actor)
actors.append(controller)

while True:
    time.sleep(2)