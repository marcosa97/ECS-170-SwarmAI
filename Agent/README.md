API TEAM PROCESS

Week 1: C++ Library

Week 2-3: PYSC2 Library
File: simple_agent.py
Run with command: python -m pysc2.bin.agent --map testing --agent simple_agent.SimpleAgent --agent_race T

Overview: This program automatically selects all the players units one by one, and moves them to another
point on the screen.
The selected unit is given a move command which determines which direction it should go.
Currently, the program is hardcoded for units to move toward the enemy when the enemy appears 
on the screens.

Functions:
extract_data():

make_move(move, x, y, enemy_x, enemy_y):
Arguments:
__move__ is a code which takes on values of 0, 1 or 2. 0 will move the unit away from the enemy, 1 will move the unit toward the enemy,
and 2 will make the unit attack the nearest enemy.
__x__ is the x coordinate of the unit
__y__ is the y coordinate of the unit
__enemy_x__ is the x coordinate of the nearest enemy unit
__enemy_y__ is the y coordinate of the nearest enemy unit
Return value:
An array of the new target point to move to of the form [x,y], where x is the new x position, and y is the new y position.

File: our_agent.py


After we managed to successfully move the unit, we realized that each unit was only able to move one step at a time. And in order for 
this move to be made, we had to first select the unit, which also required a step to be taken. Therefore a move for each unit would take 
2 steps. So, in order to make all units move at once, the number of steps that would elapse would be 2 x n , where n is the number of
units. This is obviously very inefficient, and would ruin our Machine Learning approach which attempts to maximize every unit's reward 
for making the right move simultaneously.
Another limitation that was discovered with the PYSC2 api library was that many important features were not able to be accessed. So, 
with the inability of micro-management, and lack of data to be used by our Neural Network, we realized it would be best to change 
libraries. The raw S2Clientprotocol solved both these problems, and so we transtioned to that library to continue our work.


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
4 is south, 5 is south-west, 6 is west, and 7 is north-west. If the code is larger than 7, the direction will be toward an enemy unit.
This move is made relative to the unit's current position which is given as x and y coordinates of the unit.
__x__ is the x coordinate of the unit
__y__ is the y coordinate of the unit
Return value:
A target point for the unit to move to.
