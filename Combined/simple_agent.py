from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
import copy as clone
import numpy as np
import sarah_kerrigan
import time

# define the features the AI can seee
_AI_RELATIVE = features.SCREEN_FEATURES.player_relative.index

_AI_SELF = 1

def get_marine_location(ai_relative_view):
    '''get the indices where the world is equal to 1'''
    return (ai_relative_view == _AI_SELF).nonzero()

class SimpleAgent(base_agent.BaseAgent):
    def step(self, obs):
        super(SimpleAgent, self).step(obs)

        test_state = np.zeros((1, 1,50))
        state_list = []
        for i in range(0, 10):
            state_list.append(clone.deepcopy(test_state))
    
        result = sarah_kerrigan.command(state_list)
        print(result)


        
        #ai_view = obs.observation['screen'][_AI_RELATIVE]
        #marine_x, marine_y = get_marine_location(ai_view)

        #print("x: " + str(marine_x), "y: " + str(marine_y))
        #time.sleep(0.5)
        return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])