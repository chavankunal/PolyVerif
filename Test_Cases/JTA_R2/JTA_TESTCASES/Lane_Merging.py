#!/usr/bin/env python3
#
# Copyright (c) 2019-2020 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

from distutils.spawn import spawn
from environs import Env
import lgsvl
import time
import random
import sys
import os
import math

# Taking arguments for weather parameters and scene
rain = 0
fog = 0
wetness = 0
cloudiness = 0
damage = 0
env = Env()
scene = "JTA_R2"
file = open('pid','w+')
t = os.getpid()
pid = str(t)
file.write(pid)
file.close()
sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"), env.int("LGSVL__SIMULATOR_PORT", 8181))
if sim.current_scene == scene:
    sim.reset()
else:
    sim.load(scene)


sim.set_time_of_day(18.00, False)
print(sim.time_of_day)

spawns = sim.get_spawn()
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])
up = lgsvl.utils.transform_to_up(spawns[0])

for i in range(10 * 2):
    # Create controllables in a block
    start = (
        spawns[0].position
        + (61 + (1.0 * (i // 4))) * forward
        + ( 0 + (1.0 * (i % 4))) * right
    )
    end = start + 10 * forward
    state = lgsvl.ObjectState()
    state.transform.position = start
    state.transform.rotation = spawns[0].rotation
    '''# Set velocity and angular_velocity
    state.velocity = 10 * up
    state.angular_velocity = 6.5 * right'''

    # add controllable
    o = sim.controllable_add("TrafficCone", state)


state = lgsvl.AgentState()
state.transform = spawns[0]
state.transform.position = spawns[0].position + 7 * forward + 1 * right
state.transform.rotation = spawns[0].rotation
state.velocity =8 * forward

ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", "myLexusVehicle"), lgsvl.AgentType.EGO, state)
# The EGO is now looking for a bridge at the specified IP and port
ego.connect_bridge(env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1"), env.int("LGSVL__AUTOPILOT_0_PORT", 9090))
# An EGO will not connect to a bridge unless commanded to
print("Bridge connected:", ego.bridge_connected)

sim.run(6)

#turn right
# VehicleControl objects can only be applied to EGO vehicles
# You can set the steering (-1 ... 1), throttle and braking (0 ... 1), handbrake and reverse (bool)
c = lgsvl.VehicleControl()
#c.throttle = 0.5
c.steering = -0.15
# a True in apply_control means the control will be continuously applied ("sticky"). False means the control will be applied for 1 frame
ego.apply_control(c, True)
sim.run(1.5)

c = lgsvl.VehicleControl()
c.throttle = 0.0
c.steering = 0.2
# a True in apply_control means the control will be continuously applied ("sticky"). False means the control will be applied for 1 frame
ego.apply_control(c, True)
sim.run(2)
c = lgsvl.VehicleControl()
c.throttle = 0.0
c.steering = -0.01
# a True in apply_control means the control will be continuously applied ("sticky"). False means the control will be applied for 1 frame
ego.apply_control(c, True)
sim.run(7)