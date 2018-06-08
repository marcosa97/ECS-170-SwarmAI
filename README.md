# SWARM AI: Using MARL to create a micromanagement AI

## Introduction


SCII is the new frontier in AI. It has an intractably large sample/action space, partially observable environment, and non-zero-sum competition. We believe the most promising way to create an AI for SCII is to use a chain-of-command system, where each level of command breaks down the game’s complexity into pieces, much like a divide-and-conquer strategy. Specifically for combat, there are macro and micromanagement techniques that greatly differ in scope. Based on our assumptions, to create an AI for combat would mean to have a 'commander' AI making macro tatical decisions such as army placement and skill usage, and then have another AI to deal with micro decisions, such as unit movemeent and when to attack. The goal of this project is create a micromanagement AI that can learn efficient combat decisions that mimick professional players. Such an AI system can then be used as an ‘unit’ by higher-level-command AIs such that the complexity of micro-managing units is abstracted. To implement this swarm, we are using a neural network to predict actions with the greatest value in combat. Each unit will have the same neural network as its policy, and thus it can be used for all different types of units. This will reduce complexity in terms of creating the AI.

## Theory

The idea behind this AI is to use MARL to train a policy neural network that can approximate efficient combat micromanagement for all combat-specific units. The core algorithm is called SARSA(lambda), which is an on-policy reinforcement learning algorithm. This algorithm deals with the issue of time-delayed rewards [2], which is a common issue for SCII. 

Our AI works by extending SARSA(lambda) to multiple units, but with the same policy network to predict Q-values. Because all units have the same policy, it is easier to implement (do not need to train individual polices for the huge number of unique units), and encourges cooperative behavior that is the core of micromanagement. More details are available in the Learning folder.

Due to the difficulty of the Q-value function for SCII, we decided to try a dense neural network with 7 residual layers. The architecture is shown below:

Input:
The input is a 1D array of features extracted from the game as a representation of game state. Currently we are considering two sets of features, one from the last game state, and one from current game state.

ally values (stacked in 8 directions)
ally health (stacked in 8 directions)
self-previous action
self-value
self-health
self-attack range
self-attack cooldown
self-attack damage
self.armor
target attack range
enemy values (stacked in 8 directions)
enemy distance (stacked in 8 directions)
enemy attack damage
enemy-armor
impassable terrain distance (8 dimensions)

Output:
The output consists of 9 nodes. 8 of them represent movement-type nodes, and 1 represent attack. The 8 movement nodes each encode a pi/4 radians region of the movement circle. If a movement node is chosen, a random click in a direction within the region coded to that node is executed. This is to help bots recognize “general areas to move to”, like a human player. The attack node executes an attack, but the actual attack target is issued by heuristics. This is to deal with the fact that features such as splash damage, weakness, and other features are difficult for our policy network to learn.

Thus, as one can see, the AI is mostly concerned with micromanagement such as movement and when to attack, which will then enable a tactical AI to make heuristic judgements on who to attack, what troops to send, and what skills to use, without the complexity of controlling the movement and attack time of each unit.

## Training Pipeline

The agent will be implemented as a bot script in the API. More details are available in the Agent-API folder. The entire system will be ported into Google CloudML (more details in CloudML folder), and trained using asynchronous actor-critic agents. The goal is to collect data from games by running multiple instances of the script, collecting state data, and then having the neural network train by random sampling of collected state, action and reward data. Each script worker will send collected data to a trainer worker, who owns a local database that stores the most recent data. The trainer will periodically call another trainer to take a random sample of the data and train its policy network. Once trained, new actors will be provided the updated policy network to improve decision making.

## Deliverables

The deliverables are available in each of the three folders.

## Future works

The immediate future work is to complete all feature extraction, and then import the policy network package into a game agent, and start training. Once the AI demonstrates visible improvement, the script can then be ported to Google CloudML for mass data collection and fast training.

## Sources cited:

1.Rogers, K. D., & Skabar, A. A. (2014). A Micromanagement Task Allocation System for Real-Time Strategy Games. IEEE Transactions on Computational Intelligence and AI in Games,6(1), 67-77. doi:10.1109/tciaig.2013.2297334
2. Kun Shao, K., Shu, Y., & Zhao, D. (april 2018). StarCraft Micromanagement with Reinforcement Learning and Curriculum Transfer Learning. Neural Networks (IJCNN).