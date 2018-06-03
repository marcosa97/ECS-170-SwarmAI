# Learning Environment

## Introduction

This learning environment is an implementation of an on-policy learning algorithm called SARSA(lambda), but modified for multi-agent reinforcement learning. The core algorithm is based on the MARL algorithm by Shao et. al [1]. The goal is train a powerful policy network that can approximate combat decision making on a low level, which can then abstract away certain complexities associated with micromanagement. This will then enable a higher-level symbolic AI to make decisions based on heuristics that cannot be easily learned (such as effects of skills, baiting, etc). 

## Algorithm

The algorithm consists of two steps: An action step, and then a forward propagation step.

### Pseudocode

```
def SARSA(initial_state, MAX_EPISODE_COUNT, lambda, gamma, alpha)


	while (game.end == FALSE)

		episode_count = 0

		QA_state_set = []

		new_state = initial_state

		action_vector = policy_network.predict(new_state)

		action = e_greedy_select(action_vector)

		Q_current = action_vector[action]

		while (epsisode_count < MAX_EPISODE_COUNT)

			new_state, reward = game.take_action(action) # observe new state s' and reward r
			if (game.end == FALSE)
				update_database(QA_state_set)
				return

			next_action_vector = policy_network.predict(new_state)
			next_action = e_greedy_select(next_action_vector)

			Q_next = next_action_vector[next_action]

			QA_state.action = action
			QA_state.state = new_state
			QA_state.eligibility_trace = 1 # Trace replacement
			QA_state.reward = Q_next
			QA_state_set.append(QA_state)

			delta = reward + gamma * Q_next - Q_current

			for all state in QA_state_set # Update all previously visited states

				state.reward += alpha * delta * state.eligibility_trace
				state.eligibility_trace *= gamma * lambda


			action = next_action
			episode_count ++

		update_database(QA_state_set)



```

This algorithm is edited to fit our objective. Some of the changes include:

* Trace replacement is used because of the extremely low probability of visiting the same state twice
* Policy network parameters are not updated in the algorithm, but the data from the training is saved as training data. To accomodate distributed iteration of this algorithm in an A3C training algorithm, the data is saved to a database, which will be used to train the policy network independently.
* A new while loop is added outside of the episode while loop to continuously loop the algorithm if the game is not over. If the game terminates during an action, the current data is sent to the data base, and the algorithm terminates
* In actual implementation, the algorithm is broken down into parts, and a separate state trace is saved for each unit to keep track.


### Action

The action step takes an action with every single unit, and then wait for a collective reward back from the environment. A 'delta' value is calculated as the difference between the actual and predicted score, which is then used in the forward propagation step.

### Forward Propagation

The forward propagation step goes through all the previous states starting at the first state, and update its discounted reward and eligibility trace based on the 'delta' from the action step. This is repeated until the most recent state, for all units. 

## Implementation

The framework is set up such that it can work with the SCII API in a 'throw and catch' fashion. The 'throw' function command() will take in state of the game as observed by each unit, and then return an action tensor, while saving information required for learning.


```
def command(minion_state)
# Take in all states of units
# Calculate move based on policy network and e-greedy selection
# Save predicted reward for all units
# Return action tensor

```

The 'catch' function update_reward() calculates the delta for each unit, and then update their previous states accordingly.

```
def update_reward(reward)
# Get delta for each unit based on reward
# Update the previous state_action states (QA_state) for all units
# Increment episodes

```

Once the episodes hit the maximum allowed value, or the game reaches a terminal state, the data is then packaged and saved to a database in the form QA(state, action, reward). Each QA state contains required data for training the policy network for future iterations.

## Sources

[1] https://arxiv.org/abs/1804.00810




