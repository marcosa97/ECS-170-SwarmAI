#Copyright @ ECS 170 Project team IF STMT 4 LYFE

import overlord
import numpy as np
import copy as clone

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

main()
