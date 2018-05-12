#Copyright @ ECS 170 Project team IF STMT 4 LYFE

import overlord
import numpy as np
import copy as clone


# Will add non-deterministic behavior using monomial distribution & rand
def command(minion_state):
	carrier = overlord.Command()
	command_list = []
	minion_count = len(minion_state)
	for minion in minion_state:
		command_list.append(carrier.subjugate(minion))

	return command_list

def main():
	test_state = np.zeros((1, 1,50))
	state_list = []
	for i in range(0, 10):
		state_list.append(clone.deepcopy(test_state))
	result = command(state_list)
	print(result)


# Not yet working, need to rewrite system in class form, and switch function names
def SARSA(self):
	# This gets called after action is taken, and a reward is returned
	alpha = self.alpha
	gamma = self.gamma
	lambda_ = self.lambda_
	state_vec = self.state_sets
	new_state = self.command(self.current_state)
	delta = r + gamma * self.command(new_state) - state_vec[-1].Q_val
	elig_vec = self.e_trace
	elig_vec.append(1)
	state_vec.append(new_state)

	for i in range(len(state_vec) - 1, 0):
		delta = reward_vec[i] + gamma * state_vec[i].Q_val - state_vec[i-1].Q_val
		state_vec[i-1].reward = state_vec[i].reward + alpha * delta * elig_vec[i]
		elig_vec[i-1] = gamma*lambda_*elig_vec[i] + self.reward_gradient * state_vec[i].Q_val


main()
