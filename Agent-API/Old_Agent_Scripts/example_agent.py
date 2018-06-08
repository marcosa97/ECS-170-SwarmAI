from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

#Functions
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id #creates a marine
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id

#Features
# player_relative is an array that contains a list of units arranged
# "relative" to the current player.
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

#Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLYDEPOT = 19
_TERRAN_SCV = 45
_TERRAN_BARRACKS = 21

#Parameters
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_PLAYER_SELF = 1
_NOT_QUEUED = [0]
_QUEUED = [1] 

class SimpleAgent(base_agent.BaseAgent):
    #variable to store our location: we spawn on top left of map
    #We will approximate the location of our base using the
    #mean of our units' coordinates
    base_top_left = None

    #Flags for keeping track of where we are in build order
    supply_depot_built = False
    barracks_built = False
    scv_selected = False

    #For tracking our build order
    barracks_selected = False
    barracks_rallied = False
    
    #For tracking our army control
    army_selected = False
    army_rallied = False   
 
    #obs: series of nested arrays that contains "observations", 
    #     data that lets you know where and what things are
    #Step: Moves the game one step forward
    #      TODO: See if i can modify the time unit of a step
    def step(self, obs):
        super(SimpleAgent, self).step(obs)
        
        #get location of our base
        if self.base_top_left is None:
            player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31

        #return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])
        
        #For getting an SCV to build a supply depot 
        #Note: Coordinates in the "screen" are relative to the screen,
        #      NOT the overall map
        if not self.supply_depot_built:
            if not self.scv_selected:
                #This gets the coordinates of ALL SCV units
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                #Note: coordinates of units are returned in the order y, x
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero() 
        
                #Here, we select only one unit
                target = [unit_x[0], unit_y[0]]
                
                self.scv_selected = True
                
                #The function call instructs the game to "click" the mouse at the
                #SCV's location, just like a human would to select the SCV 
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

            #Once an SCV unit is selected, tell the game to build the supply depot
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
             
                #We want to build the supply depot near the command center.
                #The command center is made up of multiple coordinates, so use mean.
                #We build the supply depot 20 units below the command center.
                target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)

                self.supply_depot_built = True

                return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_NOT_QUEUED, target])         
        elif not self.barracks_built:
            if _BUILD_BARRACKS in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                
                #We want the barracks to the right of our command center
                # (or left if our base is at bottom right)
                target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
                self.barracks_built = True

                return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])        
        elif not self.barracks_rallied:
            if not self.barracks_selected:
                #Set the rally point of the barracks to the top of our ramp
                #so we can defend ourselves until we have enough units to 
                #move out
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()
               
                #in order to select the barracks, we have to wait
                #until they're avaliable, so we check with any()
                if unit_y.any():
                    target = [int(unit_x.mean()), int(unit_y.mean())]

                    self.barracks_selected = True

                    return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            else:
                self.barracks_rallied = True
                    
                #ramp locations have been hard coded for simplicity 
                if self.base_top_left:
                    return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 21] ])
                
                return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 46] ])
        
        #Build marines
        elif obs.observation["player"][_SUPPLY_USED] < obs.observation["player"][_SUPPLY_MAX] and _TRAIN_MARINE in obs.observation["available_actions"]:
            return actions.FunctionCall(_TRAIN_MARINE, [_QUEUED])
       
        #Send amry out
        elif not self.army_rallied:
            if not self.army_selected:
                if _SELECT_ARMY in obs.observation["available_actions"]:
                    self.army_selected = True
                    self.barracks_selected = False

                    return actions.FunctionCall(_SELECT_ARMY, [_NOT_QUEUED])
            elif _ATTACK_MINIMAP in obs.observation["available_actions"]:
                self.army_rallied = True
                self.army_selected = False

                #Attack points have been hardcoded
                if self.base_top_left:
                    return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, [39, 45] ])

                return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, [21, 24] ])        

        #if none of the conditions hold, just step ahead
        return actions.FunctionCall(_NOOP, [])           



    #Helper method for working with locations relative to our base
    #  @x, y: initial x and y coordinates
    #  @x_distance, y_distance: distances to selected point from
    #                           initial x,y coordinates
    def transformLocation(self, x, x_distance, y, y_distance):
        #if our base is at bottom right, distances are subtacted, 
        #  meaning that positive distances will move the selected point
        #  closer to the top left
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]
        
        #if base is at top left, positive distances move us to the
        # bottom right
        return [x + x_distance, y + y_distance]

     
