#Copyright @ ECS 170 Project team IF STMT 4 LYFE

import overlord
import numpy as np
import copy as clone
import hive_command as hive
import math as m


class queen_of_blades:
	# Framework class

	def __init__(gamma, lambda_, alpha, episodes, unit_count)
		self.gamma = hive.gamma # SARSA gamma constant
		self.lambda_ = hive.lambda_ # SARSA lambda constant
		self.alpha = hive.alpha # SARSA learning rate
		self.episodes = 0
		self.episode_max = hive.episodes # SARSA maximum episodes
		self.QA_state_list = [] # list keeping track of Q(s,a) pairs
		self.unit_count = unit_count # Starting unit count
		self.pred_val = [0 for x in range(unit_count)] # Keep track of rewards predicted by each unit for each episode

	def command(minion_states):

		carrier = overlord.Command()

		command_list = []

		for i in range(0, len(minion_states)): # Save QA state and return command for all units
			will, pred_val[i] = assume_control(minion_states[i])
			WA_state_list.append(QA_state(minion_states[i], will))
			command_list.append(will)

		return command_list

	def assume_control(self, state)
		resist_control = np.random.uniform(0, 1, 1) # mutation to resist control encourage exploration
		epsilon = 0.5 * m.sqrt(1 + self.episodes)

		if resist_control > epsilon:
			will = carrier.subjugate(minion_state)
		else:
			will = np.random.int(10, size = 1)

		return will



	def update_reward(self, reward)
		for i in range(0, len(minion_states)):
			delta = reward + self.gamma * self.pred_val[i] - QA-state_list[i][-1].pred # Calculate delta from predicted reward
			for j in range(0, len(QA_state_list[i]))
				QA_state_list[i][j].update_state(self.gamma, self.lambda_, self.alpha, delta)

		self.episodes += 1 # Update episode count

		if episodes == 1001:
			# Export data as numpy arrays in the form of Q(state, action, actual_reward), will work with our cloudML engineer to implement



class QA_state:
	def __init__(state, choice, reward)
		self.state = state
		self.choice = choice
		self.reward = reward
		self.e_val = 1 # Using replacement strategy for eligibility trace
		self.pred = prediction

	def update_state(self, gamma, lambda_, alpha, delta)
		self.reward += alpha * delta * self.e_val # Update reward for all visited states
		self.e_val *= gamma * lambda_ # Update eligibility trace

