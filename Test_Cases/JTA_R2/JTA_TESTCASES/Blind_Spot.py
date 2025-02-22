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
env = Env()

# Taking arguments for weather parameters and scene
rain = 0
fog = 0
wetness = 0
cloudiness = 0
damage = 0
scene = "JTA_R2"
file = open('pid','w+');
t = os.getpid()
pid = str(t)
file.write(pid)
file.close()

#if sys.argv[1]: 
   #rain = float(sys.argv[1])
   #fog = float(sys.argv[2])
   #wetness = float(sys.argv[3])
   #cloudiness = float(sys.argv[4])
   #damage = float(sys.argv[5])
   #scene = sys.argv[6]

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"), env.int("LGSVL__SIMULATOR_PORT", 8181))
if sim.current_scene == scene:
    sim.reset()
else:
    sim.load(scene)

spawns = sim.get_spawn()
print(spawns)
destinations = spawns[1].destinations
print(destinations)
sim.set_time_of_day(18.00, False)
print(sim.time_of_day)

# EGO
state = lgsvl.AgentState()
forward = lgsvl.utils.transform_to_forward(spawns[1])
right = lgsvl.utils.transform_to_right(spawns[1])
up = lgsvl.utils.transform_to_up(spawns[1])

# NPC
state = lgsvl.AgentState()
state.transform.position = spawns[1].position + 10 * forward - 1 * right 
state.transform.rotation = spawns[1].rotation
npc = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, state)
npc.velocity = 19 * forward
npc.follow_closest_lane(True,25)

state.transform = spawns[1]
state.transform.position = spawns[0].position + 20 * forward - 2 * right
state.transform.rotation.y = spawns[1].rotation.y - 3
state.velocity = 10 * forward
ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", "myLexusVehicle"), lgsvl.AgentType.EGO, state)

# An EGO will not connect to a bridge unless commanded to
print("Bridge connected:", ego.bridge_connected)

# The EGO is now looking for a bridge at the specified IP and port
ego.connect_bridge(env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1"), env.int("LGSVL__AUTOPILOT_0_PORT", 9090))



# NPC
state = lgsvl.AgentState()
state.transform.position = spawns[1].position - 5 * forward + 1 * right 
state.transform.rotation = spawns[1].rotation
npc = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, state)
npc.follow_closest_lane(True,20)
#sim.run(10)

sim.run(15)