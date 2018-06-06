#TO RUN THIS AGENT:
# python -m pysc2.bin.agent --map Simple64 --agent our_agent.OurAgent --agent_race Z

#To start our agent as a Zerg race, use flag --agent_race Z 

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
import pygame
import time

#Functions
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_MOVE = actions.FUNCTIONS.Move_screen.id 
_TRAIN_QUEEN = actions.FUNCTIONS.Train_Queen_quick.id
_TRAIN_ZERGLING = actions.FUNCTIONS.Train_Zergling_quick.id
_BUILD_SPAWNINGPOOL = actions.FUNCTIONS.Build_SpawningPool_screen.id
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id

#Features
#player_relative is an array that contains a list of units arranged
#"relative" to the current player
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_SELECTED = features.SCREEN_FEATURES.selected.index #which unites are selected

#Unit IDs -> Taken from StarCraft2 Client API:
#https://github.com/Blizzard/s2client-api/blob/master/include/sc2api/sc2_typeenums.h
_ZERG_HATCHERY = 86
_ZERG_SPAWNINGPOOL = 89
_ZERG_LARVA = 151
_ZERG_ZERGLING = 105
_ZERG_DRONE = 104
_ZERG_HYDRALISK = 107
#Add ranged unit here
#Add slow melee unit here

#Parameters -> Taken from pysc2 environment info:
#https://github.com/deepmind/pysc2/blob/master/docs/environment.md
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_PLAYER_SELF = 1
_NOT_QUEUED = [0]
_QUEUED = [1]

#SOME CONSTANTS
_MAP_WIDTH = 64
_MAP_HEIGHT = 64

#NOTE: FOR TESTING FUNCTIONS FROM HUMAN INPUT
#USAGE:
#   @Press: 1-9 to return that button's number
#           Once one of these is pressed, you
#           have to press 0 to be able to return a
#           number again
#   @Press: 0 to reset input
class InputManager():
	keyPressed = False

    #Returns value of key pressed down
    #If no key is pressed down, return -1 
	def checkKeyPressed(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_1] and not self.keyPressed:
			#print("PRESSED 1")
			self.keyPressed = True
			return 1
		elif keys[pygame.K_2] and not self.keyPressed:
			self.keyPressed = True
			return 2
		elif keys[pygame.K_3] and not self.keyPressed:
			self.keyPressed = True
			return 3
		elif keys[pygame.K_4] and not self.keyPressed:
			self.keyPressed = True
			return 4
		elif keys[pygame.K_5] and not self.keyPressed:
			self.keyPressed = True
			return 5
		elif keys[pygame.K_6] and not self.keyPressed:
			self.keyPressed = True
			return 6
		elif keys[pygame.K_7] and not self.keyPressed:
			self.keyPressed = True
			return 7
		elif keys[pygame.K_8] and not self.keyPressed:
			self.keyPressed = True
			return 8
		elif keys[pygame.K_9] and not self.keyPressed:
			self.keyPressed = True
			return 9
		elif keys[pygame.K_UP] and not self.keyPressed:
			self.keyPressed = True
			return 10
		elif keys[pygame.K_DOWN] and not self.keyPressed:
			self.keyPressed = True
			return 11
		elif keys[pygame.K_LEFT] and not self.keyPressed:
			self.keyPressed = True
			return 12
		elif keys[pygame.K_RIGHT] and not self.keyPressed:
			self.keyPressed = True
			return 13
        #This is for resetting input
		if keys[pygame.K_0] and self.keyPressed:
			self.keyPressed = False
			return 0

		return -1

class OurAgent(base_agent.BaseAgent):
    #variable to store our location: we spawn on the top left of map
    #We will approximate the location of our base using the mean 
    #of our units' starting position coordinates
    base_top_left = None

    #For testing functions via user input
    inputMngr = InputManager()


    #Step: Moves the game one step forward
    #      TODO: See if i can modify the time unit of a step
    #@self: Python requres all methods of classes to 
    #       add a reference to itself, so we defune methods like this
    #@obs: series of nested arrays that contains "observations", 
    #      data that lets you know where and what things are
    def step(self, obs):
    	super(OurAgent, self).step(obs)

    	#get location of our base
    	if self.base_top_left is None:
    		player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
    		# base_top_left = map height / 2
    		self.base_top_left = player_y.mean() <= 31


    	#FOR TESTING FUNCTIONS VIA USER INPUT
        keyPressed = self.inputMngr.checkKeyPressed()
        if (keyPressed == 1):
        	print("1 PRESSED: SELECTING LARVA")
        	return self.select_larva(obs)
        elif (keyPressed == 2):
        	print("2 PRESSED: SELECTING DRONE")
        	return self.select_drone(obs)
        elif (keyPressed == 3):
        	print("3 PRESSED: BUILDING SPAWN TOOL")
        	return self.build_spawningpool(obs)
        elif (keyPressed == 4):
        	print("4 PRESSED: MOVING SELECTED UNIT TO POINT")
        	return self.move_to_point(obs)
        elif (keyPressed == 5):
        	print("5 PRESSED: TRAINING ZERGLING")
        	return self.train_zergling(obs)
        elif (keyPressed == 6):
        	print("6 PRESSED: SELECTING ZERGLING")
        	return self.select_zergling(obs)
        elif (keyPressed == 10):
        	print("UP PRESSED: MOVING UP")
        	return self.move_in_direction(obs, [0, -20])
        elif (keyPressed == 11):
        	print("DOWN PRESSED: MOVING DOWN")
        	return self.move_in_direction(obs, [0, 20])
        elif (keyPressed == 12):
        	print("LEFT PRESSED: MOVING LEFT")
        	return self.move_in_direction(obs, [-20, 0])
        elif (keyPressed == 13):
        	print("RIGHT PRESSED: MOVING RIGHT")
        	return self.move_in_direction(obs, [20, 0])

    	return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])

    #FOR TESTING MOVEMENT
    def move_to_point(self, obs):
    	if _MOVE in obs.observation["available_actions"]:
    		#Get location of the selected unit
    		selected = obs.observation["screen"][_SELECTED]

    		unit_y, unit_x = selected.nonzero()
    		x = round(unit_x.mean())
    		y = round(unit_y.mean())

    		print(unit_y)
    		print(unit_x)

    		#Choose location to move to relative to selected unit
    		target = [ x + 20, y + 20]

    		#Return function call
    		return actions.FunctionCall( _MOVE, [_NOT_QUEUED, target] )

    	else:
    		return actions.FunctionCall( _NOOP, [] )

    #NOTE: Top left corner of the map has coordinates 0, 0
    #Moves a selected unit in the direction provided in the vector
    #  @vector: an array with 2 values, [x_value, y_value]
    def move_in_direction(self, obs, vector):
    	if _MOVE in obs.observation["available_actions"]:
    		selected = obs.observation["screen"][_SELECTED]

    		unit_y, unit_x = selected.nonzero()
    		x = round(unit_x.mean())
    		y = round(unit_y.mean())

    		target_x = x + vector[0]
    		target_y = y + vector[1]

    		#Make sure we don't choose a point out of the map
    		#TODO: Crashes when a unit wanders off to far from the map
    		#  Receive the following error:
    		#  Argument is out of range for 331/Move_screen (3/queued [2]; 
    		#  0/screen [0, 0]), got: [[0], [nan, nan]]
    		if (x + vector[0]) > _MAP_WIDTH:
    			target_x = _MAP_WIDTH
    		if (y + vector[1]) > _MAP_HEIGHT:
    			target_y = _MAP_HEIGHT
    		if (x + vector[0]) < 0:
    			target_x = 0
    		if (y + vector[1]) < 0:
    			target_y = 0

    		target = [ target_x, target_y ]

    		return actions.FunctionCall( _MOVE, [_NOT_QUEUED, target] )
    	else:
    		return actions.FunctionCall( _NOOP, [] )

    def select_larva(self, obs):
    	#Get coordinates of ALL LARVA units
    	unit_type = obs.observation["screen"][_UNIT_TYPE]
    	unit_y, unit_x = (unit_type == _ZERG_LARVA).nonzero()
        
    	#Select only one unit
    	target = [ unit_x[0], unit_y[0] ]

    	#The function call instructs the game to "click" the mouse at the
    	#larva's location, just lika a human would to select it
    	return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target] )

    def select_drone(self, obs):
    	#Get coordinates of ALL DRONE units
    	unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == _ZERG_DRONE).nonzero()

        #Select only one unit
        if not unit_x.any() or not unit_y.any():
        	return actions.FunctionCall(_NOOP, [])
        else:
        	target = [ unit_x[0], unit_y[0] ]

        return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target] )

    def select_zergling(self, obs):
    	unit_type = obs.observation["screen"][_UNIT_TYPE]
    	unit_y, unit_x = (unit_type == _ZERG_ZERGLING).nonzero()
    	if not unit_x.any() or not unit_y.any():
    		return actions.FunctionCall(_NOOP, [])
    	else:
    		target = [ unit_x[0], unit_y[0] ]
    	return actions.FunctionCall( _SELECT_POINT, [_NOT_QUEUED, target] )

    def build_spawningpool(self, obs):
    	if _BUILD_SPAWNINGPOOL in obs.observation["available_actions"]:
    		unit_type = obs.observation["screen"][_UNIT_TYPE]
    		unit_y, unit_x = (unit_type == _ZERG_HATCHERY).nonzero()

    		#We want to build the spawning pool near the hatchery.
			#The hatchery is made up of multiple coordinates, so use mean.
			#HARD CODED FOR NOW: We build the spawning pool 20 units below the command center.
    		target = self.transformLocation( int(unit_x.mean()), 20, int(unit_y.mean()), 0 )

    		return actions.FunctionCall(_BUILD_SPAWNINGPOOL, [_NOT_QUEUED, target] )

    	else:
    		return actions.FunctionCall( _NOOP, [] )

    #NOTE: Larva has to be selected to use this
    #TODO: Only allow _TRAIN_ZERGLING to be returned if 
    #      there's a spawning pool built and a larva is selected
    def train_zergling(self, obs):
    	if obs.observation["player"][_SUPPLY_USED] < obs.observation["player"][_SUPPLY_MAX]:
    		if _TRAIN_ZERGLING in obs.observation["available_actions"]:
    			return actions.FunctionCall(_TRAIN_ZERGLING, [_QUEUED])

    #TODO: Create functions for training and selecting other types of units

    #TODO: Decide which specific information to extract from the game
    #Function for extracting information from the game
    #  The information will come from the "obs" object, more specifically
    #  from its obs.observation["screen"] and obs.observation["player"] components.
    #  The information that each component holds can be found here:
    #      https://github.com/deepmind/pysc2/blob/master/docs/environment.md
    def extract_game_data(self, obs):
    	game_info = [ obs.observation["screen"], obs.observation["player"] ]
    	return game_info

	#Helper method for working with locations relative to our base
	#  @x, y: initial x and y coordinates
	#  @x_distance, y_distance: distances to selected point from
	#                           initial x,y coordinates
	#TAKEN FROM: Steven Brown (skjb)'s "Building a Basic Agent" Tutorial
    def transformLocation(self, x, x_distance, y, y_distance):
    	#if our base is at bottom right of the map, distances are subtacted, 
		#  meaning that positive distances will move the selected point
		#  closer to the top left
    	if not self.base_top_left:
    		return [x - x_distance, y - y_distance] 

    	#if base is at top left, positive distances move us to the 
    	# bottom right
    	return [x + x_distance, y - y_distance]


