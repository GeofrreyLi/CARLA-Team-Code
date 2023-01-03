import glob
import os
import sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
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

IM_WIDTH = 640
IM_HEIGHT = 480


def process_img(image, str):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow(str, i3)
    cv2.waitKey(1)
    # cc = carla.ColorConverter.LogarithmicDepth
    image.save_to_disk('_out/%06d.png' % image.frame)
    return i3/255.0


actor_list = []
try:
    client = carla.Client('localhost', 2000) # https://carla.readthedocs.io/en/0.9.11/core_world/#the-client
    client.set_timeout(2.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library() # https://carla.readthedocs.io/en/0.9.11/core_actors/#blueprints

    bp = blueprint_library.filter('model3')[0]
    print(bp)

    ##
    # spawn_point = random.choice(world.get_map().get_spawn_points())
    spawn_point = carla.Transform(carla.Location(x=-127.812881, y=-127.425674, z=0.300000), carla.Rotation(pitch=0.000000, yaw=90.393547, roll=0.000000))
    print(spawn_point)

    vehicle = world.spawn_actor(bp, spawn_point)
    vehicle.apply_control(carla.VehicleControl(throttle=0.1, steer=0.0))
    # vehicle.set_autopilot(True)  # if you just wanted some NPCs to drive.

    actor_list.append(vehicle)


    #
    z = 18
    spawn_point1 = carla.Transform(carla.Location(x=-105, y=-213.5, z=z), carla.Rotation(pitch=-0.000000, yaw=90.393547, roll=0.000000))
    print(spawn_point1)
    r_bp =blueprint_library.find('static.prop.colacan')
    r1 = world.spawn_actor(r_bp, spawn_point1)
    actor_list.append(r1)



    #
    spawn_point2 = carla.Transform(carla.Location(x=-120, y=-213.5, z=z), carla.Rotation(pitch=-0.000000, yaw=90.393547, roll=0.000000))
    print(spawn_point2)
    r2 = world.spawn_actor(r_bp, spawn_point2)
    actor_list.append(r2)

    spawn_point3 = carla.Transform(carla.Location(x=-135, y=-213.5, z=z), carla.Rotation(pitch=-0.000000, yaw=90.393547, roll=0.000000))
    print(spawn_point3)
    r3 = world.spawn_actor(r_bp, spawn_point3)
    actor_list.append(r3)

    spawn_point4 = carla.Transform(carla.Location(x=-150, y=-213.5, z=z), carla.Rotation(pitch=-0.000000, yaw=85.393547, roll=0.000000))
    print(spawn_point4)
    r4 = world.spawn_actor(r_bp, spawn_point4)
    actor_list.append(r4)

    # spawn_point5 = carla.Transform(carla.Location(x=-150, y=-213.5, z=0), carla.Rotation(pitch=-0.000000, yaw=84.393547, roll=0.000000))
    # print(spawn_point5)
    # r5 = world.spawn_actor(r_bp, spawn_point5)
    # actor_list.append(r5)

    # spawn_point6 = carla.Transform(carla.Location(x=-150, y=-213.5, z=0), carla.Rotation(pitch=-0.000000, yaw=84.0, roll=0.000000))
    # print(spawn_point6)
    # r6 = world.spawn_actor(r_bp, spawn_point6)
    # actor_list.append(r6)

    
    # get the blueprint for this sensor: https://carla.readthedocs.io/en/0.9.11/core_sensors/#sensors-step-by-step
    cam_bp = blueprint_library.find('sensor.camera.rgb')
    # change the dimensions of the image
    cam_bp.set_attribute('image_size_x', f'{IM_WIDTH}')
    cam_bp.set_attribute('image_size_y', f'{IM_HEIGHT}')
    cam_bp.set_attribute('fov', '110')

    

    # Adjust sensor relative to vehicle
    spawn_point = carla.Transform(carla.Location(x=0, y=0, z=0), carla.Rotation(pitch=-42.000000, yaw=0, roll=0))
    # spawn the sensor and attach to vehicle.
    sensor1 = world.spawn_actor(cam_bp, spawn_point, attach_to=r1)
    # add sensor to list of actors
    actor_list.append(sensor1)
    # do something with this sensor
    sensor1.listen(lambda data: process_img(data, "sensor1"))


    sensor2 = world.spawn_actor(cam_bp, spawn_point, attach_to=r2)
    actor_list.append(sensor2)
    sensor2.listen(lambda data: process_img(data, "sensor2"))


    sensor3 = world.spawn_actor(cam_bp, spawn_point, attach_to=r3)
    actor_list.append(sensor3)
    sensor3.listen(lambda data: process_img(data, "sensor3"))


    sensor4 = world.spawn_actor(cam_bp, spawn_point, attach_to=r4)
    actor_list.append(sensor4)
    sensor4.listen(lambda data: process_img(data, "sensor4"))

    # sensor5 = world.spawn_actor(cam_bp, spawn_point, attach_to=r5)
    # actor_list.append(sensor5)
    # sensor5.listen(lambda data: process_img(data, "sensor5"))

    # sensor6 = world.spawn_actor(cam_bp, spawn_point, attach_to=r6)
    # actor_list.append(sensor6)
    # sensor6.listen(lambda data: process_img(data, "sensor6"))


    # # get the blueprint for this sensor: https://carla.readthedocs.io/en/0.9.11/core_sensors/#sensors-step-by-step
    # cam_bp2 = blueprint_library.find('sensor.camera.rgb')
    # # change the dimensions of the image
    # cam_bp2.set_attribute('image_size_x', f'{IM_WIDTH}')
    # cam_bp2.set_attribute('image_size_y', f'{IM_HEIGHT}')
    # cam_bp2.set_attribute('fov', '110')

    # # Adjust sensor relative to vehicle
    # spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    # # spawn the sensor and attach to vehicle.
    # sensor2 = world.spawn_actor(cam_bp2, spawn_point, attach_to=r2)

    # # add sensor to list of actors
    # actor_list.append(sensor2)

    # # do something with this sensor
    # sensor2.listen(lambda data: process_img(data))

    time.sleep(180)

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')