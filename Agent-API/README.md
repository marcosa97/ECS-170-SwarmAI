# Agent API Team's Work and Contributions
API Contributors:
  -Marcos Alcantar
  -Natalie Bashenko
  -Tu-Ning Ting
  -Aaron Jenkins

As the Agent API team for this project, we were in charge of implementing a wrapper around the Starcraft II game's client API to make interfacing and communicating between our team's Neural Network and the game easier. In the end, we ended up using a modified version of Hannes Karppila's (@Dentosal) Starcraft II API Client for Python 3, which utilizes Blizzard's sc2 protobuf protocol. 

## Linux Setup
To set up the envorinment for the agent script to run in Linux, you will need to have the StarCraft II full game version 3.17. The game will have to live in ~/StarCraftII/ . 

You can follow Blizzard's documentation for the Linux version here: https://github.com/Blizzard/s2client-proto#downloads  
Again, make sure you download VERSION 3.17.

You will need to download the Melee map pack as well.  


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
