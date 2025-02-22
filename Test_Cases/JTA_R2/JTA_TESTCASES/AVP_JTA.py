#!/usr/bin/env python3
#
# Copyright (c) 2019-2020 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

from environs import Env
import lgsvl
import time
import random
import sys
import os
from pathlib import Path
env = Env()

# Taking arguments for weather parameters and scene
rain = 0
fog = 0
wetness = 0
cloudiness = 0
damage = 0
scene = "JTA_R2"
home = str(Path.home())
file = open(home+'/pid','w');
t = os.getpid()
pid = str(t)
file.write(pid)
file.close()
print("pid : ",pid)
if sys.argv[1]: 
   rain = float(sys.argv[1])
   fog = float(sys.argv[2])
   wetness = float(sys.argv[3])
   cloudiness = float(sys.argv[4])
   damage = float(sys.argv[5])
   scene = sys.argv[6]

print("Running Scenario in which there is no Vehicle available in any Lane")
sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"), env.int("LGSVL__SIMULATOR_PORT", 8181))
if sim.current_scene == scene:
    sim.reset()
else:
    sim.load(scene)


sim.set_time_of_day(18, True)
print(sim.time_of_day) 


#sim.weather = lgsvl.WeatherState(rain, fog, wetness, cloudiness, damage)

spawns = sim.get_spawn()
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])


state = lgsvl.AgentState()
#state.transform = spawns[0]
state.transform.position = spawns[0].position - 4 * right    # -2
state.transform.rotation.y = spawns[0].rotation.y + 2.5
#state.transform.position = spawns[0].position - 5 * right
#state.transform.rotation = spawns[0].rotation
# state.velocity = 10 * forward
# tr = spawns[0]
# t1 = sim.map_from_gps(
#     northing=4137773.15130157,
#     easting=596690.508709717,
#     altitude=-19.1056592464447,
#     orientation=310,
# )
# print("Transform from northing/easting: {}".format(t1))

# state.transform = t1
ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", "myLexusVehicle"), lgsvl.AgentType.EGO, state)

# An EGO will not connect to a bridge unless commanded to

# The EGO is now looking for a bridge at the specified IP and port
#ego.connect_bridge(env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1"), env.int("LGSVL__AUTOPILOT_0_PORT", 9090))
ego.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)
print("Bridge connected:", ego.bridge_connected)

# for i, name in enumerate(["SUV", "Jeep", "SUV"]):
#     state1 = lgsvl.AgentState()
#     state1.transform.position = spawns[0].position + (20 * forward) - (4.0 * i * right) # + 10.0 * forward
#     state1.transform.rotation = spawns[0].rotation
#     npc = sim.add_agent(name, lgsvl.AgentType.NPC, state1)
#     npc.follow_closest_lane(True, 12)

#input("press Enter to run ")
sim.run()

# t0 = time.time()
# sim.run(time_limit=60, time_scale=1)
# t1 = time.time()
# sim.stop()
