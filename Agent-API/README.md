# Agent API Team's Work and Contributions
API Contributors:
  -Marcos Alcantar
  -Natalie Bashenko
  -Tu-Ning Ting

As the Agent API team for this project, we were in charge of implementing a wrapper around the Starcraft II game's client API to make interfacing and communicating between our team's Neural Network and the game easier. In the end, we ended up using a modified version of Hannes Karppila's (@Dentosal) Starcraft II API Client for Python 3, which utilizes Blizzard's sc2 protobuf protocol. 

## Linux Setup
To set up the envorinment for the agent script to run in Linux, you will need to have the StarCraft II full game version 3.17. The game will have to live in ~/StarCraftII/ . 

You can follow Blizzard's documentation for the Linux version here: https://github.com/Blizzard/s2client-proto#downloads  
Again, make sure you download VERSION 3.17.

## Map
You will need to download the Melee map pack. You can find the instructions provided in the Blizzard's documentation.  

Additionally, you can create any custom map by using the Windows version of StarCraft II. The application is called Map Editor, which is in the same directory as the StarCraft II executable is. By using Map editor, you can do many things such as setting your spawn places, setting the units you would like to have in the beginning of the game, and adding terrains, and so on. Moreover, you are also allowed to change the data, such as the hit points and moving speed of a kind of unit.

We used the Map Editor to create a custom map called **testing.SC2MAP**, to test our agent. In this map, it is a plain map (without any terrains or height). Additionally, there are two ally units (Hydralisk) and one enemy unit (Zergling). The hit points of Zergling is increased twice of its original health and the moving speed is decreased twice of its original health. The reason of changing the data of Zergling is because in our project, we are training ranged ally units to efficiently attack melee enemy units. In StarCraft II, Zergling is a melee unit. However, originally Zergling is a high-speed and low-damage units. It is not a good choice to train our SwarmAI. Therefore, by reversing its properties, the Zergling will be the best enemy units we would like to simulate our AI.

#CAUTION#
When we created the **testing** custom map, there was some error messages popping up when we try to run our agent on the custom map. After digging the issue, we figured out that we need to change the **trigger** when we used the Map Editor. In the Map Editor, there is a **trigger** section, where you can modify some conditions, such as the winning conditions. In this section, we delete the winning conditions, so that when we run our agent on the map, the game will not terminate itself immediately (because our custom map only contains two Hydralisks and one Zergling, without any workers or buildings, therefore the game is in *terminating* state automatically).


##TIMELINE: API TEAM PROCESS

Week 1: C++ Library

Week 2-3: PYSC2 Library File: simple_agent.py Run with command: python

Functions: extract_data():

make_move():

File: our_agent.py

After we managed to successfully move the unit, we realized that each unit was only able to move one step at a time. And in order for this move to be made, we had to first select the unit, which also required a step to be taken. Therefore a move for each unit would take 2 steps. So, if we had multiple units,

Week 4-5: S2clientprotocol Library File: new_agent3.py Run with command: python3 new_agent3.py Must first replace old unit.py and data.py files with new ones to be able to extract all the data.

Functions: extract_data():

make_move2(move, x, y): Arguments: move is a code that is given to a unit to determine which direction it should travel. We have 8 directional movement so the codes range from 0 to 7, where 0 is north, 1 is north-east, 2 is east, 3 is south-east, 4 is south, 5 is south-west, 6 is west, and 7 is north-west. This move is made relative to the unit's current position which is given as x and y coordinates of the unit. x is the x coordinate of the unit y is the y coordinate of the unit Return value: A target point for the unit to move to.
