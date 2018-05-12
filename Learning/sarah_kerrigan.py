#Copyright @ ECS 170 Project team IF STMT 4 LYFE

import overlord
import numpy as np
import copy as clone
import hive_command as hive


class queen_of_blades:
	def __init__(gamma, lambda_, alpha, episodes)
		self.gamma = hive.gamma # SARSA gamma constant
		self.lambda_ = hive.lambda_ # SARSA lambda constant
		self.alpha = hive.alpha # SARSA learning rate
		self.episodes = hive.episodes # SARSA maximum episodes
		self.Q_state_list = [] # list keeping track of Q(s,a) pairs

	def command(minion_state):

		carrier = overlord.Command()

		command_list = []

		for minion_state in minion_states:
			will = carrier.subjugate(minion_state)
			Q_state_list.append(Q_state(minion, will))
			command_list.append(will)

		return command_list

	def SARSA(self):

	def update_reward(self, reward)




class Q_state:
	def __init__(state, choice, reward)
		self.state = state
		self.choice = choice
		self.reward = reward
		self.e_val = 1

	def update_state(self, gamma, lambda_, alpha, delta)
		self.reward += alpha * delta * self.e_val
		self.e_val *= gamma * lambda_






def main():
	test_state = np.zeros((1, 1,50))
	state_list = []
	for i in range(0, 10):
		state_list.append(clone.deepcopy(test_state))
	result = command(state_list)
	print(result)


main()
