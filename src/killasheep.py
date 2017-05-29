import MalmoPython
import os
import sys
import time
import random
import json
from math import sqrt
from collections import defaultdict

TURN_VELOCITY = 0.5

class ReinforcementLearningModel:
	def __init__(self, gamma=0.8):
		self._q_table = defaultdict(dict)
		self._previous_action = None
		self._previous_state = None
		self._gamma = gamma

	def _get_sheep_distances(self, a):
		#a = json.loads(obs)
		#print type(a[0])
		me = (0, 0)
		sheeps = []
		for x in a:
			if x['name'].count('Killer') > 0:
				me = (int(x['x']), int(x['y']))
		for x in a:
			if x['name'].count('Killer') == 0:
				sheep = (x['x'], x['y'])
				distance = sqrt((sheep[0] - me[0]) ** 2 + (sheep[1] - me[1]) ** 2)
				if distance < 1:
					sheeps.append(0)
				elif distance < 10:
					sheeps.append(1)
				else:
					sheeps.append(2)
		return tuple(sorted(sheeps))	

	def _select_action(self, q_raw, eps, actions):
		a = min(q_raw.keys(), key=lambda x: q_raw[x])
		return random.choice(actions) if random.random() < eps else random.choice([x for x in actions if q_raw[x] == q_raw[a]])

	def _update_q_table(self, state):
		if self._previous_state is None or self._previous_action is None:
			return
		self._q_table[self._previous_state][self._previous_action] += 100 * (len(state) < len(self._previous_state)) + self._gamma * (max(self._q_table[state].values()) if len(self._q_table[state]) != 0 else 0)

	def get_action(self, obs):
		state = self._get_sheep_distances(obs)
		self._update_q_table(state)
		actions = ['turn 45', 'turn 90', 'turn 135', 'turn 180', 'turn 225', 'turn 270', 'turn 315']
		actions += ['move'] * len(actions)
		if state[0] == 0:
			actions.append('attack')
		q_raw = self._q_table[state]
		for action in actions:
			if not action in q_raw:
				q_raw[action] = 0
		self._previous_action = self._select_action(q_raw, 0.2, actions)
		self._previous_state = state
		print self._previous_action
		return self._previous_action

	def restart(self):
		self._q_table[self._previous_state][self._previous_action] += 1000
		self._previous_action = None
		self._previous_state = None

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

NUM_GOALS = 20
GOAL_TYPE = "apple"
GOAL_REWARD = 100
ARENA_WIDTH = 60
ARENA_BREADTH = 60
GROUND_LVL = 207
MOB_TYPE = "Sheep"  # Change for fun, but note that spawning conditions have to be correct - eg spiders will require darker conditions.

def getItemXML():
    ''' Build an XML string that contains some randomly positioned goal items'''
    xml=""
    for item in range(NUM_GOALS):
        x = str(random.randint(-ARENA_WIDTH/2,ARENA_WIDTH/2))
        z = str(random.randint(-ARENA_BREADTH/2,ARENA_BREADTH/2))
        xml += '''<DrawItem x="''' + x + '''" y="210" z="''' + z + '''" type="''' + GOAL_TYPE + '''"/>'''
    return xml

def getCorner(index,top,left,expand=0,y=206):
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+ARENA_WIDTH/2)) if left else str(expand+ARENA_WIDTH/2)
    z = str(-(expand+ARENA_BREADTH/2)) if top else str(expand+ARENA_BREADTH/2)
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'

def spawn_ebaniy_mob():
    random.seed(time.time())
    return ' x="' + str(random.randint(-ARENA_WIDTH/2, ARENA_WIDTH/2)) + '" y="' + str(GROUND_LVL) + \
        '" z="' + str(random.randint(-ARENA_WIDTH/2, ARENA_WIDTH/2)) + '" '

def getMissionXML(summary):
    ''' Build an XML mission string.'''
    spawn_mob = 'type="Sheep"'
    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + summary + '''</Summary>
        </About>

        <ModSettings>
            <MsPerTick>20</MsPerTick>
        </ModSettings>
        <ServerSection>
            <ServerInitialConditions>
                <Weather>clear</Weather>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <AllowSpawning>true</AllowSpawning>
                <AllowedMobs>Sheep</AllowedMobs>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
                <DrawingDecorator>
                    <DrawCuboid ''' + getCorner("1",True,True,expand=1) + " " + getCorner("2",False,False,y=226,expand=1) + ''' type="stone"/>
                    <DrawCuboid ''' + getCorner("1",True,True,y=207) + " " + getCorner("2",False,False,y=226) + ''' type="air"/>

                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>
                    <DrawEntity ''' + spawn_ebaniy_mob() + spawn_mob + '''/>

                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Fucking Sheep Killer</Name>
            <AgentStart>
                <Placement x="0" y="207" z="0"/>
                <Inventory>
                    <InventoryItem slot="0" type="diamond_sword"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ChatCommands/>
                <ContinuousMovementCommands turnSpeedDegs="360"/>
                <AbsoluteMovementCommands/>
                <ObservationFromFullStats/>
                <ObservationFromGrid>
                      <Grid name="floorAll">
                        <min x="-30" y="0" z="-30"/>
                        <max x="30" y="0" z="30"/>
                      </Grid>
                </ObservationFromGrid>
                <ObservationFromNearbyEntities> 
                    <Range name="EntityObservations" xrange="30" yrange="1" zrange="30"/>
                </ObservationFromNearbyEntities>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

def load_grid(world_state):
    """
    Used the agent grid map observation API to get a ...x... grid box around the agent (the agent is in the middle).

    Args
        world_state:    <object>    current agent world state

    Returns
        grid:   <list>  the world grid blocks represented as a list of blocks
    """
    while world_state.is_mission_running:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            open('map_state.txt', 'w').write(str(observations))
            grid = observations.get(u'floorAll', 0)
            break
    return grid

def load_entity_observations(world_state):
    """
    Used the agent entity observation API to get a ...x... grid box around the agent (the agent is in the middle).

    Args
        world_state:    <object>    current agent world state

    Returns
        obs:   <list>  the world grid which represents the entities around yourself inclusevly
        (
            e.g. sample obs with one entity {u'name': u'Sheep', u'yaw': -136.40625, u'pitch': 0.0, u'y': 207.0, u'x': 27.447916666666664, u'z': -8.416666666666668}
            yaw: rotation around y axis
            pitch: probably doesn't matter
            y: vertical
            x: ->
            z:  |
                V
                    yaw=180
            yaw=90          yaw=-90
                    yaw=0

        )
    """
    while world_state.is_mission_running:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            obs = observations.get(u'EntityObservations', 0)
            break
    return obs

def get_yaw(world_state):
    while world_state.is_mission_running:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')
        if world_state.number_of_observations_since_last_state > 0:
            observations = json.loads(world_state.observations[-1].text)
            entities = observations.get(u'EntityObservations', 0)
            for entity in observations.get(u'EntityObservations', 0):
                if entity.get(u'name', 0) == u'Fucking Sheep Killer':
                    return entity.get(u'yaw')

def turn(agent_host, degrees):
    yaw = int(get_yaw(agent_host.getWorldState()))
    final_yaw = yaw + degrees
    direction = 1
    if final_yaw >= 360:
        final_yaw -= 360
        direction = -1
    while yaw < final_yaw if direction == 1 else yaw > final_yaw:
        agent_host.sendCommand('turn ' + str(direction*TURN_VELOCITY))
        yaw = int(get_yaw(agent_host.getWorldState()))
    agent_host.sendCommand('turn 0')

def perform_action(agent_host, action, prev_action):
    if prev_action:
        agent_host.sendCommand(prev_action + ' 0')
    action_parsed = action.split(' ')
    if action_parsed[0] == 'turn':
        turn(agent_host, int(action_parsed[1]))
    elif action_parsed[0] == 'move':
        agent_host.sendCommand('move 1')
    else:
        agent_host.sendCommand('attack')
    return action_parsed[0]

agent_host = MalmoPython.AgentHost()

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
prev_action = None
# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    #grid = load_grid(world_state)                       #returns a grid map
    obs = load_entity_observations(world_state)
    action = model.get_action(obs)
    prev_action = perform_action(agent_host, action, prev_action)
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"