import time
import random
import json

import config


def getCorner(index,top,left,expand=0,y=206):
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+config.ARENA_WIDTH/2)) if left else str(expand+config.ARENA_WIDTH/2)
    z = str(-(expand+config.ARENA_BREADTH/2)) if top else str(expand+config.ARENA_BREADTH/2)
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'


def spawn_ebaniy_mob():
    random.seed(time.time())
    return ' x="' + str(random.randint(-config.ARENA_WIDTH/2 + 1, config.ARENA_WIDTH/2 - 1)) + '" y="' + str(config.GROUND_LVL) + \
        '" z="' + str(random.randint(-config.ARENA_WIDTH/2 + 1, config.ARENA_WIDTH/2 - 1)) + '" '


def getMissionXML(summary):
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
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
                        <DrawEntity ''' + spawn_ebaniy_mob() + 'type="' + config.MOB_TYPE + '''" />
			<DrawEntity ''' + spawn_ebaniy_mob() + 'type="' + config.MOB_TYPE + '''" />
			<DrawEntity ''' + spawn_ebaniy_mob() + 'type="' + config.MOB_TYPE + '''" />
			

                    </DrawingDecorator>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
            </ServerSection>

            <AgentSection mode="Survival">
                <Name>Killer</Name>
                <AgentStart>
                    <Placement x="0.5" y="207" z="0.5" yaw="0"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_sword"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <ContinuousMovementCommands/>          
                    <AbsoluteMovementCommands/>
                    <ChatCommands/>
                    <ObservationFromFullStats/>
                    <VideoProducer>
                        <Width>200</Width>
                        <Height>200</Height>
                    </VideoProducer>
                    <ObservationFromGrid>
                        <Grid name="floorAll">
                            <min x="''' + str(-1*config.ARENA_WIDTH / 2) + '''" y="0" z="''' + str(-1*config.ARENA_BREADTH / 2) + '''"/>
                            <max x="''' + str(config.ARENA_WIDTH / 2) + '''" y="0" z="''' + str(config.ARENA_BREADTH / 2) + '''"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromNearbyEntities> 
                        <Range name="EntityObservations" xrange="''' + str(config.ARENA_WIDTH) + '''" yrange="1" zrange="''' + str(config.ARENA_BREADTH) + '''"/>
                    </ObservationFromNearbyEntities>
                </AgentHandlers>
            </AgentSection>
        </Mission>'''


# <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
# <Placement x="0.5" y="56.0" z="0.5" yaw="0"/> setYaw 90
                #     <!-- <ContinuousMovementCommands/> <DiscreteMovementCommands /> -->              
                # <!-- <AbsoluteMovementCommands/> -->

# def getMissionXML(summary):
#     ''' Build an XML mission string.'''
#     return '''<?xml version="1.0" encoding="UTF-8" ?>
#     <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
#         <About>
#             <Summary>''' + summary + '''</Summary>
#         </About>

#         <ModSettings>
#             <MsPerTick>20</MsPerTick>
#         </ModSettings>
#         <ServerSection>
#             <ServerInitialConditions>
#                 <Weather>clear</Weather>
#                 <Time>
#                     <StartTime>1000</StartTime>
#                     <AllowPassageOfTime>false</AllowPassageOfTime>
#                 </Time>
#                 <AllowSpawning>true</AllowSpawning>
#                 <AllowedMobs>Sheep</AllowedMobs>
#             </ServerInitialConditions>
#             <ServerHandlers>
#                 <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
#                 <DrawingDecorator>
#                     <DrawCuboid ''' + getCorner("1",True,True,expand=1) + " " + getCorner("2",False,False,y=226,expand=1) + ''' type="stone"/>
#                     <DrawCuboid ''' + getCorner("1",True,True,y=207) + " " + getCorner("2",False,False,y=226) + ''' type="air"/>

#                     <DrawEntity ''' + spawn_ebaniy_mob() + 'type="' + config.MOB_TYPE + '''" />
#                     <DrawEntity ''' + spawn_ebaniy_mob() + 'type="' + config.MOB_TYPE + '''" />

#                 </DrawingDecorator>
#                 <ServerQuitWhenAnyAgentFinishes />
#             </ServerHandlers>
#         </ServerSection>

#         <AgentSection mode="Survival">
#             <Name>Fucking Sheep Killer</Name>
#             <AgentStart>
#                 <Placement x="0" y="207" z="0"/>
#                 <Inventory>
#                     <InventoryItem slot="0" type="diamond_sword"/>
#                 </Inventory>
#             </AgentStart>
#             <AgentHandlers>
#                 <DiscreteMovementCommands/>
#                 <ChatCommands/>
#                 <ObservationFromFullStats/>
#                 <ObservationFromGrid>
#                       <Grid name="floorAll">
#                         <min x="''' + str(-1*config.ARENA_WIDTH / 2) + '''" y="0" z="''' + str(-1*config.ARENA_BREADTH / 2) + '''"/>
#                         <max x="''' + str(config.ARENA_WIDTH / 2) + '''" y="0" z="''' + str(config.ARENA_BREADTH / 2) + '''"/>
#                       </Grid>
#                 </ObservationFromGrid>
#                 <ObservationFromNearbyEntities> 
#                     <Range name="EntityObservations" xrange="30" yrange="1" zrange="30"/>
#                 </ObservationFromNearbyEntities>
#             </AgentHandlers>
#         </AgentSection>

#     </Mission>'''

# <ContinuousMovementCommands turnSpeedDegs="360"/>
# <AbsoluteMovementCommands/>

def load_grid(agent_host, world_state):
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


def load_entity_observations(agent_host, world_state):
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
