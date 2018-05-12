# Learning Environment

## Introduction

This learning environment is an implementation of an on-policy learning algorithm called SARSA(lambda), but modified for multi-agent reinforcement learning. The core algorithm is based on the MARL algorithm by Shao et. al [1]. The goal is train a powerful policy network that can approximate combat decision making on a low level, which can then abstract away certain complexities associated with micromanagement. This will then enable a higher-level symbolic AI to make decisions based on heuristics that cannot be easily learned (such as effects of skills, baiting, etc). 

## Algorithm

The algorithm consists of two steps: An action step, and then a forward propagation step.

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

## Work in Progress

* Work with cloudML to implement database storage operation

* Connect framework with SCII API, and finalize NN architecture

* Preliminary training 

## Sources

[1] https://arxiv.org/abs/1804.00810




