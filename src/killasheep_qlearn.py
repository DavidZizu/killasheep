import MalmoPython
import os
import sys
import time
import random
import json
from math import *
from collections import defaultdict

from world import getMissionXML, load_entity_observations, load_grid
from actions import perform_action
import config

#Calculates the angle between two vector
def angle(a,b):
	result = atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])
	return result

class ReinforcementLearningModel:
	def __init__(self, gamma=0.1, alpha=0.4, epsilon=0.2):
		self._q_table = defaultdict(dict)
		self._previous_action = None
		self._previous_state = None
		self._gamma = gamma
		self._alpha = alpha
		self._epsilon = epsilon
		self.read_model()
		print ">" * 100, "Read data - ", self._q_table


	def _save_model(self):
		print self._q_table
		with open('model.json', 'w') as f:
			f.write(json.dumps({'qtable': {repr(s): self._q_table[s] for s in self._q_table}}))


	def read_model(self):
		if 'model.json' not in os.listdir('.'):
			return
		with open('model.json', 'r') as f:
			data = json.loads(f.read())['qtable']
		for x in data:
			self._q_table[eval(x)] = {int(y): data[x][y] for y in data[x]}


	def _get_sheep_distances(self, obs):
		me = (0, 0)
		sheeps = []
		coordinates = []
		for x in obs:
			if x['name'] == 'Killer':
				me = (float(-x['x']), float(x['z']))
				yaw = int(x['yaw'])
				yaw_vector = (sin(yaw / (180 / pi)), cos(yaw / (180 / pi)))
				break
		for x in obs:
			if x['name'] == config.MOB_TYPE:
				sheep = (-x['x'], x['z'])
				coordinates.append(sheep)
				distance = sqrt((sheep[0] - me[0]) ** 2 + (sheep[1] - me[1]) ** 2)
				if distance <= 1.2:
					sheeps.append(0)
				elif distance < 5:
					sheeps.append(1)
				else:
					sheeps.append(2)
		return (tuple(sheeps), coordinates, me, yaw_vector, yaw)

	def _select_action(self, q_raw, eps, actions):
		print q_raw, actions, '<' * 10
		a = min(q_raw.keys(), key=lambda x: q_raw[x])
		return random.choice(actions) if random.random() < eps else random.choice([x for x in actions if q_raw[x] == q_raw[a]])

	def _update_q_table(self, state):
		if self._previous_state is None or self._previous_action is None:
			return
		to_add = 100 if len(state) < len(self._previous_state) else -2
		self._q_table[self._previous_state][self._previous_action] += to_add + self._gamma * (max(self._q_table[state].values()) if len(self._q_table[state]) != 0 else 0)

	def _turn_action_into_movement(self, me, vision_vector, sheep, yaw):
		distance = sqrt((sheep[0] - me[0]) ** 2 + (sheep[1] - me[1]) ** 2)
		s = (-me[0] + sheep[0], -me[1] + sheep[1])
		t = angle(vision_vector, s) * (180 / pi)
		print "My coordinates: {}, Sheep coordinates: {}, Vision vector: {}, Sheep vector: {}, Angle: {}, Yaw: {}".format(me, sheep, vision_vector, s, t, yaw)
		if abs(t) <= 45.001:
			if distance <= 1.2:
				return "attack"
			return "move 1"
		elif t < 0:
			return "turn -1"
		else:
			return "turn 1"

	def get_action(self, obs):
		# return "attack"
		state, sheeps, me, yaw, angle = self._get_sheep_distances(obs)
		self._update_q_table(state)
		self._save_model()
		if len(state) == 0:
			exit(0)
		actions = list(range(len(state)))
		q_raw = self._q_table[state]
		for action in actions:
			if not action in q_raw:
				q_raw[action] = 0
		self._previous_action = self._select_action(q_raw, 0.2, actions)
		self._previous_state = state
		result = self._turn_action_into_movement(me, yaw, sheeps[self._previous_action], angle)
		print result
		return result

	def restart(self):
		self._q_table[self._previous_state][self._previous_action] += 1000
		self._previous_action = None
		self._previous_state = None


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

def get_pitch(agent_host, world_state):
	while world_state.is_mission_running:
		world_state = agent_host.getWorldState()
		if len(world_state.errors) > 0:
			raise AssertionError('Could not load grid.')
		if world_state.number_of_observations_since_last_state > 0:
			observations = json.loads(world_state.observations[-1].text)
			entities = observations.get(u'EntityObservations', 0)
			for entity in observations.get(u'EntityObservations', 0):
				if entity.get(u'name', 0).count('Killer') != 0:
					return (int(entity.get(u'pitch')))

def tilt_head(agent_host, world_state):
	pitch = get_pitch(agent_host, agent_host.getWorldState())
	init_pitch = pitch
	final_pitch = 30
	agent_host.sendCommand("pitch " + str(config.TURN_VELOCITY))
	while pitch < final_pitch:
		pitch = get_pitch(agent_host, agent_host.getWorldState())
	agent_host.sendCommand("pitch 0")


if __name__=='__main__':
	agent_host = MalmoPython.AgentHost()

	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

	try:
		agent_host.parse( sys.argv )
	except RuntimeError as e:
		print 'ERROR:',e
		print agent_host.getUsage()
		exit(1)
	if agent_host.receivedArgument("help"):
		print agent_host.getUsage()
		exit(0)


	my_mission = MalmoPython.MissionSpec(getMissionXML('Kill Fucking Sheep'), True)
	my_mission_record = MalmoPython.MissionRecordSpec()
	my_mission.requestVideo(800, 500)
	my_mission.setViewpoint(1)

	# Attempt to start a mission:
	max_retries = 3
	for retry in range(max_retries):
		try:
			agent_host.startMission( my_mission, my_mission_record )
			break
		except RuntimeError as e:
			if retry == max_retries - 1:
				print "Error starting mission:",e
				exit(1)
			else:
				time.sleep(2)

	# Loop until mission starts:
	print "Waiting for the mission to start ",
	world_state = agent_host.getWorldState()
	while not world_state.has_mission_begun:
		sys.stdout.write(".")
		time.sleep(0.1)
		world_state = agent_host.getWorldState()
		for error in world_state.errors:
			print "Error:",error.text

	print
	print "Mission running ",

	model = ReinforcementLearningModel()

	count = 0
	tilt_head(agent_host, world_state)
	# Loop until mission ends:
	while world_state.is_mission_running:
		sys.stdout.write(".")
		time.sleep(0.1)
		world_state = agent_host.getWorldState()
		obs = load_entity_observations(agent_host, world_state)             #get all the objects that are in the map
		action = model.get_action(obs)
		print obs

		if action.split(' ')[0] == 'move':
			perform_action(agent_host, action)
		elif action.split(' ')[0] == 'turn':
			init_yaw = get_yaw(agent_host, world_state)
			delta_yaw = 270 if int(action.split(' ')[1]) > 0 else 90
			final_yaw = init_yaw + delta_yaw
			if final_yaw >= 360:
				final_yaw -= 360
			agent_host.sendCommand("setYaw " + str(final_yaw))
		else:
			agent_host.sendCommand("attack 1")
			time.sleep(1)
			agent_host.sendCommand("attack 0")

		time.sleep(0.1)
		world_state = agent_host.getWorldState()
		for error in world_state.errors:
			print "Error:",error.text

	print
	print "Mission ended"
