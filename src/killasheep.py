import MalmoPython
import os
import sys
import time
import random
import json

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
                    <InventoryItem slot="1" type="diamond_sword"/>
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
        grid:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)
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
        obs:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)
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

# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    #grid = load_grid(world_state)                       #returns a grid map
    obs = load_entity_observations(world_state)
    print obs
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"