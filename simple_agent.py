'''
This program automatically selects all the players units one by one, and moves them to another
point on the screen
The selected unit is given a move command which determines which direction it should go.
Currently, the program is hardcoded for units to move toward the enemy when the enemy appears 
on the screens

***IMPORTANT***
FOR PLAYING SIMPLEMAP 64, CHANGE LINE 41 to 64, AND LINE 145 to unit_type == _HYDRALISK
FOR PLAYING testing map, CHANGE LINE 41 to 48 AND LINE 145 to unit_type == _SCV

Command to Run: python -m pysc2.bin.agent --map testing --agent simple_agent.SimpleAgent --agent_race T
'''

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
import math
from sklearn.cluster import KMeans
import numpy as np


#features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
#Unit id
_TERRAN_COMMANDCENTER = 18
_HYDRALISK = 107
_SCV = 45
#player relative attributes
_PLAYER_SELF = 1
_PLAYER_HOSTILE = 4
#Functions
_SELECT_POINT = actions.FUNCTIONS.select_point.id # selects the unit at a specified point
_NOOP = actions.FUNCTIONS.no_op.id #default--no action
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id # moves the selected unit to a specified point
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id # causes selected unit to attack at a specified point
_NOT_QUEUED = [0]
#Screen attributes
_MIN_SCREEN_SZ = 0
_MAX_SCREEN_SZ = 48 # for our custom testing map; 64 for Simple64 Map

# One action is performed every step, and a single unit's move is an action
#Therefore for all units to move "simultaneously" we probably need to keep all the units 
#stored globally and keep a count of which unit is next--essentially it will wait in a 
# queue for their turn-- this is what units_loc will hold
#A move first requires a unit to be selected. And selecting a unit is an action.
# therfore, For a move to occur for one unit will require 2 "steps".
# and for n units, to move all units, we need 2*n steps.
class SimpleAgent(base_agent.BaseAgent):
	unit_selected = False
	unit_moved = False
	units_loc =[] #holds the coordinates of all the ally units
	unit_ind = 0 
	attack = False
	enemy_loc = [] #holds coordinates for enemy units


	'''
	make_move takes in a selected units x and y coordinates, and a move:
	move of 0 is for move backward, away from enemy
	move of 1 is move toward enemy
	move of 2 is attack enemy
	movements are determined by comparing the distances NESW of the unit with the 
	enemy location
	'''
	def make_move(self, move, x, y):
		distance = 10 # how far to move in x and y direction
		enemy_x = self.enemy_loc[0]
		enemy_y = self.enemy_loc[1]
		north_y = y + distance
		south_y = y - distance
		east_x = x + distance
		west_x = x - distance
		# Conditions to avoid having an out of bound coordinate
		if north_y < _MIN_SCREEN_SZ:
			north_y = _MIN_SCREEN_SZ
		if south_y < _MIN_SCREEN_SZ:
			south_y = _MIN_SCREEN_SZ
		if east_x < _MIN_SCREEN_SZ:
			east_x = _MIN_SCREEN_SZ
		if west_x < _MIN_SCREEN_SZ:
			west_x = _MIN_SCREEN_SZ

		if north_y > _MAX_SCREEN_SZ:
			north_y = _MAX_SCREEN_SZ
		if south_y > _MAX_SCREEN_SZ:
			south_y = _MAX_SCREEN_SZ
		if east_x > _MAX_SCREEN_SZ:
			east_x = _MAX_SCREEN_SZ
		if west_x > _MAX_SCREEN_SZ:
			west_x = _MAX_SCREEN_SZ

		if ( abs(enemy_x - east_x) > abs(enemy_x - west_x)):
			targetx0 = east_x
			targetx1 = west_x
			print("east")
		else:
			targetx0 = west_x
			targetx1 = east_x
			print("west")
		if ( abs(enemy_y - north_y) > abs(enemy_y - south_y)):
			targety0 = north_y
			targety1 = south_y
			print("north")
		else:
			targety0 = south_y
			targety1 = north_y
			print("south")

		if move == 0: #back
			#targety = y - distance
			#targetx = x - distance
			target = [ targetx0, targety0]

		elif move == 1: #forward
			target = [targetx1, targety1]
			#target = [x + distance, y + distance]

		else: #move =2, attack
			attack = True
			target = [enemy_x, enemy_y]#[x,y]
		return target

	def step(self, obs):
		super(SimpleAgent, self).step(obs)
		#print (obs.observation['screen'][_PLAYER_RELATIVE])
		#print("obs type: " + str(type(obs)))
		#print("obs.observation['screen'] type: " + str(type(obs.observation['screen'])))
		#print("obs.observation['player'] type: " + str(type(obs.observation['player'])))
		#print("obs.observation['screen'] type: " + str(obs.observation['screen'].shape))
		#print("obs.observation['player'] type: " + str(obs.observation['player'].shape))

		#unit_type will give a matrix the size of the screen with all units
		#player_relative is the same but categorized 1 for friendly, 4 for enemy.
		unit_type = obs.observation['screen'][_UNIT_TYPE]
		player_relative = obs.observation['screen'][_PLAYER_RELATIVE]
		print("unit_type")
		print(_UNIT_TYPE)
		cc_y,cc_x =  (unit_type == _TERRAN_COMMANDCENTER).nonzero()
		ps_y,ps_x = (player_relative == _PLAYER_SELF).nonzero() #(unit_type == _TERRAN_COMMANDCENTER).nonzero()
		ph_y,ph_x = (player_relative == _PLAYER_HOSTILE).nonzero()
		#Use _SCV for Simple64 Map,
		# Or _HYDRALISK for the testing map.
		hy_y, hy_x = (unit_type == _HYDRALISK).nonzero()
		# 12.0 is how many pixels the unit takes up on the screen
		# it is different for different units (9.0 for _SCV)
		# *number in denominator must be a float*
		hydralisk_count = int(math.ceil(len(hy_y) / 12.0))
		#units holds all coordinates of all units of the ally
		units = []
		for i in range(0, len(hy_y)):
			units.append((hy_x[i], hy_y[i]))
		print("units")
		print(units)
		print("hydralisk_count")
		print(hydralisk_count)
		# Using KMeans, we can find the center coordinates of each unit, and reduce our total 
		# coordinates used from the units variable above.
		# It is only updated when the unit_ind is back at 0, in other words, when all units 
		# have already been moved in the queue.
		kmeans = KMeans(n_clusters=hydralisk_count)
		if len(units) > 0 and self.unit_ind == 0:
			kmeans.fit(units)
			self.units_loc = kmeans.cluster_centers_
			print("clusters")
			print(self.units_loc)


		print("ENEMY")
		print(ph_x)
		print(ph_y)

		#an array of coordinates on which the command center lies
		cc_p = zip(cc_x,cc_y) 
		#an array of coords on which the player's friendly team lies
		ps_p = zip(ps_x,ps_y) 
		#hostile coords
		h_x = round(ph_x.mean())
		h_y = round(ph_y.mean())
		#ph_p = zip(ph_x,ph_y)
		self.enemy_loc = [h_x, h_y]
		# array to hold all units - command center.
		# example: Each unit will take up 9 points, so for 12 units, we'll get 
		# an array of 108 coordinates.
		units_coord = []  

		for point in ps_p:
			if point not in cc_p:
				units_coord.append(point)

		# if self.unit_ind == 0: #5:
		# 	self.units_loc = units_coord

		print("units_loc")
		print(self.units_loc)
		print("enemy_loc")
		print(self.enemy_loc)
		''' '''
		if _SELECT_POINT in obs.observation["available_actions"] and len(self.units_loc) >0:    
			if not self.unit_selected:

				# target is [x,y] of (x,y) in the unit_loc
				target = [ self.units_loc[self.unit_ind][0], self.units_loc[self.unit_ind][1] ]
				self.unit_selected = True
				self.unit_moved = False
				return actions.FunctionCall(_SELECT_POINT,[_NOT_QUEUED, target])
			else: #unit is selected
				if not self.unit_moved and _MOVE_SCREEN in obs.observation["available_actions"]:
					'''
					need a function to determine where the best target for this unit will be
					move north, move south, move west , move east
					'''
					# move = someArray of move actions 0,1,2
					move = 1
					target = self.make_move(move,self.units_loc[self.unit_ind][0], self.units_loc[self.unit_ind][1])
					if self.attack and _ATTACK_SCREEN in obs.observation["available_actions"]:
						#need to find nearest enemy to attack
						# target = get_nearest_enemy_loc(units_loc[unit_ind][0], units_loc[unit_ind][1]
						self.attack = False
						self.unit_moved = True
						self.unit_selected = False
						self.unit_ind = (self.unit_ind + 1) % len(self.units_loc)

						return actions.FunctionCall(_ATTACK_SCREEN, [_NOT_QUEUED, target])

					self.unit_moved = True
					self.unit_selected = False
					self.unit_ind = (self.unit_ind + 1) % len(self.units_loc)
					
					return actions.FunctionCall(_MOVE_SCREEN,[_NOT_QUEUED, target])

		'''		
		print("cc_p")
		print(cc_p)
		print("ps_p")
		print(ps_p)
		#print("ps_x")
		#print(ps_x)
		#print("ps_y")
		#print(ps_y)
		print("units_coord")
		print(units_coord)
		print("units length")
		print(len(units_coord))
		print("_PLAYER_RELATIVE")
		print(_PLAYER_RELATIVE)
		print("obs.observation['player'] type: ") 
		print(obs.observation['player'])
		print(len(obs.observation.keys()))
		'''
		return actions.FunctionCall(_NOOP, [])

#def extract_data():

'''
initialize(): Start the game, on an empty map the size of approximately the
 computer screen, with 1 ally ranged unit and 1 slow melee unit of choice. 
 Pauses the game initially.

extract_data(): Extract two sets of game data, one for ally, one for enemy. 
This data includes all units in vision and their properties.

make_move(move_vector): Unpauses the game, makes the moves according to 
move vector (same order as provided units in extract_data), 
and pauses the game again.

Move encoding: 0 to go forward, 1 to go back, 2 to attack closest enemy unit. 
All we need for now.

save_replay(): Save the game as a replay.
'''