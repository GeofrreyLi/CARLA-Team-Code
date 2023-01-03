#!/usr/bin/env python

# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


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
    return i3 / 255.0


client = carla.Client('localhost', 2000)  # https://carla.readthedocs.io/en/0.9.11/core_world/#the-client
client.set_timeout(10.0)

world = client.get_world()

blueprint_library = world.get_blueprint_library()
# vehicle = blueprint_library.filter('model3')[0]
vehicle = blueprint_library.find('vehicle.tesla.model3')
sensor = blueprint_library.find('sensor.camera.rgb')

r_bp = blueprint_library.find('static.prop.colacan')

# spawn points
spawn_points = world.get_map().get_spawn_points()[10]

# change the dimensions of the image
sensor.set_attribute('image_size_x', f'{IM_WIDTH}')
sensor.set_attribute('image_size_y', f'{IM_HEIGHT}')
sensor.set_attribute('fov', '110')

# spawn vehicle
actor_vehicle = world.spawn_actor(blueprint=vehicle, transform=spawn_points)
# get the relative coordinates of the created car
spawn_point_car = carla.121Transform(carla.Location(x=0.6, y=-0.45, z=1.6))
# spawn the sensor
actor_sensor = world.spawn_actor(blueprint=sensor, transform=spawn_point_car,
                                 attach_to=actor_vehicle)

# get real-time points from the vehicle
actor_sensor.listen(lambda data: process_img(data, "sensor2"))
actor_vehicle.set_autopilot(True)
x_list_vehicle = []
y_list_vehicle = []
z_list_vehicle = []
x_list_senor = []
y_list_senor = []
z_list_senor = []

for i in range(20):
    actor_vehicle_get = actor_vehicle.get_transform()
    actor_sensor_get = actor_sensor.get_transform()
    coordinate_sensor__str = "(x,y,z) = ({},{},{})".format(actor_sensor_get.location.x, actor_sensor_get.location.y,
                                                           actor_sensor_get.location.z)
    # put real-time coordinates in lists
    x_list_vehicle.append(actor_vehicle_get.location.x)
    y_list_vehicle.append(actor_vehicle_get.location.y)
    z_list_vehicle.append(actor_vehicle_get.location.z)
    x_list_senor.append(actor_sensor_get.location.x)
    y_list_senor.append(actor_sensor_get.location.y)
    z_list_senor.append(actor_sensor_get.location.z)
    # sleep each 5 seconds
    time.sleep(5)

# draw the plot of  real-time coordinates
fig1 = plt.figure()
ax1 = fig1.gca(projection='3d')
ax1.set_title('vehicle')
plot1 = ax1.plot(x_list_vehicle, y_list_vehicle, z_list_vehicle, label="vehicle")
plt.savefig("vehicle.png")

plt.clf()


fig2 = plt.figure()
ax2 = fig2.gca(projection='3d')
ax2.set_title('sensor')
plot2 = ax2.plot(x_list_senor, y_list_senor, z_list_senor, label="sensor")
plt.savefig("sensor.png")








