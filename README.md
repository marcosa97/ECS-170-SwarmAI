# ECS 170 Project: SwarmAI

## Conceptual Outline
For this project, our idea is to create a new type of AI called the swarm AI. Inspiration for this AI comes from the lore for the Zergs in SCII. Zergs can sense each other's presence within a range, and thus execute coordinated attacks without actual instructions on strategy. Instead, their "will" are overidden by an Overlord, which points them to a target, but does not specify method. In this context, the Overlord can be some type of "Master AI" that focuses on major decisions during a battle, while the "Swarm AI" are swarms of units assigned to certain tasks. Each member in a swarm can coordinate with each other and carry out the task efficiently. In this project, we will attempt to create such a Swarm AI.

## Neural network Architecture

To create such a Swarm AI, we decided to experiment with using a deep recurrent neural network with residual layers. We assume a swarm of 5 units, each with its own copy of this neural network. The same weights are shared for the entire swarm. Each neural network will take in previous action of the swarm (attack or retreat for all members), and this network's corresponding unit's status data (health, attack range, damage, etc), as well as data of target (health, attack damage, attack range, etc). This AI is only meant to test out this idea, so extended features such as unique skills are not taken into account. The output of the neural network consists of an attack head and a retreat head. Both heads are tanh-activated. The greater out of the two gets chosen. The physical meaning of the output values are prediction of evaluation score. The score is evaluated as follows:
- Died: -1
- Did not do damage, took damage: -0.5
- Did damage, took damage: 0
- Did not do damage, did not take damage: 0.5
- Did damage, did not take damage: 1

Number of layers, regularization constant, and other tuning parameters will be decided later on after prototyping.

## Training Pipeline

To train this neural network, we will be using an A3C, implemented to run on Google Cloud. Each action of each member of the swarm is saved as training data, with real ouputs acquired from training. The training data is stored in a database, from which the neural network will randomly sample to train continuously. 

In terms of the actual game, training is done using hydralisks and (some other ranged) as swarm units, with a melee unit as enemy. The melee unit is invincible, and will continuously pursue the swarm until it kills all of them, and then data from the session is collected and saved to databsae. Ranged units are used because it is easier to verify if the neural network is working, since behavior such as kiting and spreading out should occur as the neural network figures out how to maximize damage done and minimize damage taken.


