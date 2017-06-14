import time
import json
from copy import copy
import math

import config


def get_yaw(agent_host, world_state):
    while world_state.is_mission_running:
        # time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')
        if world_state.number_of_observations_since_last_state > 0:
            observations = json.loads(world_state.observations[-1].text)
            entities = observations.get(u'EntityObservations', 0)
            for entity in observations.get(u'EntityObservations', 0):
                if entity.get(u'name', 0).count('Killer') != 0:
                    return int(entity.get(u'yaw'))

def get_xy(agent_host, world_state):
    while world_state.is_mission_running:
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')
        if world_state.number_of_observations_since_last_state > 0:
            observations = json.loads(world_state.observations[-1].text)
            entities = observations.get(u'EntityObservations', 0)
            for entity in observations.get(u'EntityObservations', 0):
                if entity.get(u'name', 0).count('Killer') != 0:
                    return (int(entity.get(u'x')), int(entity.get(u'z')))

def turn(agent_host, degrees):
    yaw = get_yaw(agent_host, agent_host.getWorldState())
    init_yaw = yaw
    final_yaw = yaw + degrees
    direction = 1
    if final_yaw >= 360:
        final_yaw -= 360
        direction = -1
    while yaw < final_yaw if direction == 1 else yaw > final_yaw:
        # print 'current:', yaw, '; final_yaw:', final_yaw
        agent_host.sendCommand('turn ' + str(direction*config.TURN_VELOCITY))
        yaw = get_yaw(agent_host, agent_host.getWorldState())
    agent_host.sendCommand('turn 0')

    if config.DEBUG:
        print 'Initial:', init_yaw, '; Final should be:', final_yaw, '; Final actual:', yaw

def move(agent_host):
    old_x, old_y = get_xy(agent_host, agent_host.getWorldState())
    prev_x, prev_y = old_x, old_y
    x, y = copy(old_x), copy(old_y)
    agent_host.sendCommand('move ' + str(config.STRAIGHT_VELOCITY))
    while (x - old_x) ** 2 + (y - old_y) ** 2 < 1:
        x, y = get_xy(agent_host, agent_host.getWorldState())
        # if x == prev_x and y == old_y:
        #     perform_action(agent_host, "turn 180")
        #     agent_host.sendCommand('move 0')
        #     break
    agent_host.sendCommand('move 0')
    print 'old: ', old_x, ', ', old_y, '; new:', x, y

def perform_action(agent_host, action):
    action_parsed = action.split(' ')
    if action_parsed[0] == 'turn':
        turn(agent_host, 270 if int(action_parsed[1]) > 0 else 90)
    elif action_parsed[0] == 'move':
        move(agent_host)
    else:
        agent_host.sendCommand('attack')
    return action_parsed[0]