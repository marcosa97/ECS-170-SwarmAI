# Agent API Team's Work and Contributions
API Contributors:
  -Marcos Alcantar
  -Natalie Bashenko
  -Tu-Ning Ting

As the Agent API team for this project, we were in charge of implementing a wrapper around the Starcraft II game's client API to make interfacing and communicating between our team's Neural Network and the game easier. In the end, we ended up using a modified version of Hannes Karppila's (@Dentosal) Starcraft II API Client for Python 3, which utilizes Blizzard's sc2 protobuf protocol. 

## Linux Setup
To set up the envorinment for the agent script to run in Linux, you will need to have the StarCraft II full game version 3.17. The game will have to live in ~/StarCraftII/ . 

You can follow Blizzard's documentation for the Linux version here: https://github.com/Blizzard/s2client-proto#downloads  
Again, make sure you download **VERSION 3.17**, or you will not be able to run the replay.

## Map
You will need to download the Melee map pack. You can find the instructions provided in the Blizzard's documentation.  

Additionally, you can create any custom map by using the Windows version of StarCraft II. The application is called Map Editor, which is in the same directory as the StarCraft II executable is. By using Map editor, you can do many things such as setting your spawn places, setting the units you would like to have in the beginning of the game, and adding terrains, and so on. Moreover, you are also allowed to change the data, such as the hit points and moving speed of a kind of unit.

We used the Map Editor to create a custom map called **testing.SC2MAP**, to test our agent. In this map, it is a plain map (without any terrains or height). Additionally, there are two ally units (Hydralisk) and one enemy unit (Zergling). The hit points of Zergling is increased twice of its original health and the moving speed is decreased twice of its original health. The reason of changing the data of Zergling is because in our project, we are training ranged ally units to efficiently attack melee enemy units. In StarCraft II, Zergling is a melee unit. However, originally Zergling is a high-speed and low-damage units. It is not a good choice to train our SwarmAI. Therefore, by reversing its properties, the Zergling will be the best enemy units we would like to simulate our AI.

**CAUTION**

When we created the **testing** custom map, there was some error messages popping up when we try to run our agent on the custom map. After digging the issue, we figured out that we need to change the **trigger** when we used the Map Editor. In the Map Editor, there is a **trigger** section, where you can modify some conditions, such as the winning conditions. In this section, we delete the winning conditions, so that when we run our agent on the map, the game will not terminate itself immediately (because our custom map only contains two Hydralisks and one Zergling, without any workers or buildings, therefore the game is in *terminating* state automatically).


## Timeline

Week 1: C++ Library
File:
Run using VisualStudio

Overview: With multiple tutorials, resources available, and universal familiarity of C++ by our API team, we began our work using the 
Starcraft C++ Library. After the first week, however, we realized there would be difficulty interfacing the two different programming
languages code with each other. We therefore aborted use of this api, and moved on to one that was python based.

Week 2-3: PYSC2 Library
File: simple_agent.py
Run with command: python -m pysc2.bin.agent --map testing --agent simple_agent.SimpleAgent --agent_race T

Overview: This program automatically selects all the players units one by one, and moves them to another
point on the screen. 
The selected unit is given a move command which determines which direction it should go.
Currently, the program is hardcoded for units to move toward the enemy when the enemy appears 
on the screens.

Functions:

	make_move takes in a selected units x and y coordinates, and a move:
	move of 0 is for move backward, away from enemy
	move of 1 is move toward enemy
	move of 2 is attack enemy
	movements are determined by comparing the distances NESW of the unit with the 
	enemy location
make_move(move, x, y):
Arguments:
__move__ is a code which takes on values of 0, 1 or 2. 0 will move the unit away from the enemy, 1 will move the unit toward the enemy,
and 2 will make the unit attack the nearest enemy.
__x__ is the x coordinate of the unit
__y__ is the y coordinate of the unit

Return value:
An array of the new target point to move to of the form [x,y], where x is the new x position, and y is the new y position.

  The step function is called every frame and returns an action for the selected units. Within this function, we also find various 
  features that were to be useful in our NN. Unit positions were given by a list of pixels. Since units typically take up more than
  one pixel on the screen, we used K-Means Clustering to find the center of every unit's position. And since only one unit is given
  an action at every step, the units were held in an array, with the new array being evaluated after all units had been looped through.
step(obs):
Arguments:
__obs__ describes the observation of the screen at the current step and can be used to find features.
Return value:
An action for that unit: Current actions are 1) selecting the unit, 2) moving the unit to a designated point that is calculated using
the make_move function, 3) making the unit attack the nearest enemy.



File: our_agent.py


After we managed to successfully move the unit, we realized that each unit was only able to move one step at a time. And in order for 
this move to be made, we had to first select the unit, which also required a step to be taken. Therefore a move for each unit would take 
2 steps. So, in order to make all units move at once, the number of steps that would elapse would be 2 x n , where n is the number of
units. This is obviously very inefficient, and would ruin our Machine Learning approach which attempts to maximize every unit's reward 
for making the right move simultaneously.
Another limitation that was discovered with the PYSC2 api library was that many important features were not able to be accessed. So, 
with the inability of micro-management, and lack of data to be used by our Neural Network, we realized it would be best to change 
libraries. The raw S2Clientprotocol solved both these problems, and so we transitioned to that library to continue our work.


Week 4-5: S2clientprotocol Library
File: new_agent3.py
Run with command: python3 new_agent3.py
Must first replace old unit.py and data.py files with new ones to be able to extract all the data.

Functions:
  
extract_data(unit):
Argument: 
__unit__ is a unit to extract data from
Return Value:
An array of all the relevant data of that unit that will help the unit make
'smart' movements in our NN.
[name, tag, visibility, postion, direction it is facing, radius, 
 detection range, radar range, cloak, if it is blip, if it is powered,
 if it is burrowed, its current health, its maximum health, its current shield,
 its maximum shield, its energy, its maximum energy, its attributes (a list),
 the cost necessary to make the unit in minerals, (and) vespene, the time it takes
 to make the unit, its movement speed, its armor, its weapon cooldown, 
 its x coordinate, its y coordinate, the weapon range, the weapon damage, and
 the weapon speed]

make_move2(move, x, y):
Arguments:
__move__ is a code that is given to a unit to determine which direction it should travel.
We have 8 directional movement so the codes range from 0 to 7, where 0 is north, 1 is north-east, 2 is east, 3 is south-east,
4 is south, 5 is south-west, 6 is west, and 7 is north-west. If the code is larger than 7, the direction will be toward an enemy unit.
This move is made relative to the unit's current position which is given as x and y coordinates of the unit.
__x__ is the x coordinate of the unit
__y__ is the y coordinate of the unit
Return value:
A target point for the unit to move to.

  Every step the enemy's location is calculated. Then It loops through all the 
  ally units and calls the extract_data function to get all the data. Then it uses this
  data as input to the NN to compute a move vector, in the same order as the array of
  unit data. Finally, another loop through the units is done to give each one an individual
  move that will maximize their reward.
on_step(iteration):
Argument:
__iteration__ is the current step of the game
Return value: a movement for every unit which could be either an action or just 
a move. 


Conclusion:
Had there not been the several weeks spent learning and implementing Starcraft Libraries that could not accomplish
what we had intended with micromanaging units to be used in a Neural Network written in Python, we would made further progress
in using the api. For instance, one thing we had initially hoped to implement to improve our model was to divide our unit's 
surrounding space into 8 sectors. Within each of these sectors, we would calculate the sum of the health of all the enemy units.
The sector with the largest sum would be the direction that our unit would move away from when making a retreat. 
Another thing that we would have worked on given more time would be to extract more data. While the Dentosal library eased our 
ability to make progress using the s2Clientprotocol, it did not provide all data/features that are available in the original library. 
While we had found a way to add to Dentosal's library for extracting features such as a weapon's cooldown, range, speed and damage,
things like unit density were much more difficult to integrate into the code. This would have been a useful feature to have in order
to determine the best possible location our unit should travel to in order to have the best AOE (Area of Effect) damage.
