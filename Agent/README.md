API TEAM PROCESS

Week 1: C++ Library

Week 2-3: PYSC2 Library
File: simple_agent.py
Run with command: python

Functions:
extract_data():

make_move():

File: our_agent.py


After we managed to successfully move the unit, we realized that each unit was only able to move one step at a time. And in order for this
move to be made, we had to first select the unit, which also required a step to be taken. Therefore a move for each unit would take 2 steps.
So, if we had multiple units, 

Week 4-5: S2clientprotocol Library
File: new_agent3.py
Run with command: python3 new_agent3.py
Must first replace old unit.py and data.py files with new ones to be able to extract all the data.

Functions:
extract_data():

make_move2(move, x, y):
Arguments:
__move__ is a code that is given to a unit to determine which direction it should travel.
We have 8 directional movement so the codes range from 0 to 7, where 0 is north, 1 is north-east, 2 is east, 3 is south-east,
4 is south, 5 is south-west, 6 is west, and 7 is north-west.
This move is made relative to the unit's current position which is given as x and y coordinates of the unit.
__x__ is the x coordinate of the unit
__y__ is the y coordinate of the unit
Return value:
A target point for the unit to move to.
