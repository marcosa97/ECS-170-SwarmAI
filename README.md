Our AI approach:

Sample illustration, from Kun Shao et al. [2]

SCII is the new frontier in AI. It has an intractably large sample/action space, partially observable environment, and non-zero-sum competition. We believe the most promising way to create an AI for SCII is to use a chain-of-command system, where each level of command breaks down the game’s complexity into pieces, much like a divide-and-conquer strategy. As the first step, which is the focus of this project, we are making an AI ‘swarm’ of 5 units that is capable of efficient combat. Such an AI system can then be used as an ‘unit’ by higher-level-command AIs such that the complexity of micro-managing units is abstracted. To implement this swarm, we are using a neural network to predict actions with the greatest value in combat. Each unit will have the same NN, and thus it can be used for all different types of units. This will reduce complexity in terms of creating the AI.

Scope:

To make this project feasible, we are narrowing the scope such that terrain conditions will not be considered (although FOW will be). Also, the NN will not take into consideration cooldowns, unique abilities, and restrictions (some units cannot attack air, etc). The AI will consider unit type (melee/ranged) in terms of distance difference. For example, one of the input into the NN will be a 1-dimensional value representing difference between this unit’s attack range and distance from attack target, and another would be difference between target’s attack range and distance to this unit. The goal of this project is to configure a policy of combat units, where regardless of type, they can efficiently organize attacks on targets with nearby units.

Considerations:

-Time efficiency:
AI is useless if it cannot be used in a dynamic environment. Thus, we will discretize time, and make a move every set interval. Each unit has its own neural network, and thus open the room for parallelization.

-Novel approach:
We are investigating the use of deep-neural networks and how it performs against neural networks with only 1 hidden layer (used by [2]), with a new reward function that is more intuitive. We are also going to attempt to train the AI using self-play.
 



Neural Network Architecture:

Our idea is to apply RL to create an AI that can effectively engage in combat. Thus, our neural network will be designed to a multi-headed NN. Since there is no discernible correlation between input attributes and their location, we will be using a dense neural network with residual layers instead of CNN. The residual layers will help focus on certain features and prevent vanishing-gradient. This neural network will be used as our Q-value approximator.

Tentative architecture:

We will start with a baseline neural network (Input layer: TBD nodes, 2 hidden layers: 64 nodes, 1 output layer: 9 nodes). As we do further preliminary analysis, we can then modify the architecture (splitting 9 nodes into two heads for the two types of actions, adding more layers, adding residual layers, etc.)

Input:
The input is a 1D array of features extracted from the game as a representation of game state. Currently we are considering two sets of features, one from the last game state, and one from current game state. Specific representation of the input array will be decided later.
Some features that we are considering:
ally values (5 dimensions for 5 units), criterion of value will be discussed in evaluation
ally health (5 dimension for 5 units)
ally previous action (5 dimension for 5 units), each action probably will be embedded into a vector or simply 1 hot encoding)
ally distance (5 dimensions for 5 units)
self-value (1 dimension)
self-health (1 dimension)
self-previous action (1 dimension), same as previous action
self-attack range difference (1 dimension) (difference between attack range and enemy distance)
self-attack animation cooldown (1 dimension), normalized
enemy previous action (1 dimension), same as previous action
enemy value (1 dimension)
enemy distance (1 dimension)
enemy attack range distance (1 dimension) (difference between enemy’s attack range and distance away)
enemy attack damage (1 dimension)
impassable terrain (8 dimension, 1 for each “region” of the circle, divided into pi/4 sized regions)
Other features TBD.

Output:
The output consists of 11 nodes. 8 of them represent movement-type nodes, and 3 represent attacks. The 8 movement nodes each encode a pi/4 radians region of the movement circle. If a movement node is chosen, a random click in a direction within the region coded to that node is executed. This is to help bots recognize “general areas to move to”, like a human player. The attack nodes are decided based on heuristics. One is to attack the weakest, another to attack highest valued, and last to attack closest. We think these heuristics are good at approximating what professional players do.

Evaluation:

The reward function is based on economic power. Each unit in SCII has a cost related to it in terms of minerals and gas. The sum of resources used will be a unit’s value. Each time there is an altercation, the reward is based on the difference in unit values after the altercation. Damage done will be converted to value, by calculating the damage done with respect to the value of the unit, and thus same damage to a higher-valued unit will be worth more compared to a cheaper unit, etc. In the same way, damage taken by a higher-valued ally unit will cost more than same damage to a lower-valued ally. this will hopefully encourage altruistic behavior. The centralized Q function will be based on the cumulative reward of all units. The value based on damage dealt is multiplied by a factor of enemy’s total value over own’s total value. Thus, doing more with less value is encouraged.

Training Pipeline:

Our idea for creating this Swarm AI is to utilize a centralized Q-function as well as learning. The goal is to create a powerful policy approximator using the neural network that can be used for all types of units (melee or ranged, etc.). Since each agent (unit) will have the same policy parameters, they will follow the same policy. This eliminates the need for inter-agent communication, since everyone assumes every other person is using the same policy. We are currently not considering support units since they violate the identical policy assumption and incorporating them into the same policy training very difficult (very different goals). They can be trained separately using another policy system just for non-combat units, with hard-coded rules to encode their skills and abilities.

When playing the game, states and actions are chosen by the policy approximator. The agents will carry out the action with the best Q-value. Frame skip is then applied so that the next state will be 0.2s after the current state has executed its actions. The next state is then evaluated to generate a reward, which is saved as a set Q(state, action, reward). Every 5 (tentative) seconds, the game will propagate its reward using SARSA(lambda), and this is considered 1 episode. This will deal with time-delayed reward. Q set from one episode is sent to a database, and the game continues with a new episode with the next state as the new initial state. This process is repeated until game ends (all enemies die). We are also thinking of using a ‘wave’ system where after all enemy units die, the game will release more units, and training continues until ally units die. Then, the game restarts. The neural network will take random samples from the most recent 100,000 Q sets to train. Batch size and epoch size are not yet set. This system will be implemented as an asynchronous time critic in google cloud, where worker nodes will run replays of the game, and another node use a GPU to constantly update the parameters in the neural network through randomly sampling of the Q set database.

Misc. Information on training:

To improve convergence rate, we will be using a progressing learning method to train our policy network, that goes from simple scenarios to more complicated ones. The stages are tentative.
Stage 1: 1 ranged unit vs. 1 melee unit. Goal: Learn to kite.
Stage 2: 2 ranged units vs. 1 melee unit. Goal: Learn to kite with some cooperation
Stage 3: 2 ranged units vs. 1 melee unit, with obstacles. Goal: Learn to associate movement problems with the terrain data input
Stage 4: 3 ranged units vs. 1 ranged AOE unit. Goal: Learn to disperse to minimize damage against high-valued range units
Stage 5: 4 ranged units and 1 cheap melee vs. 1 fast melee with high damage unit. Goal: Learn to get the fast melee to attack the cheap melee, so the overall return is greater.
Stage 6: 5 randomly composed units and 3 random enemies.
Stage 7: Initial self-play trial, 5 vs 5.
Stage 8: Greater scale combat scenarios, such as 30 vs 30, with self-play to avoid overfitting to default AI behavior

Further stages depend on training result, and if there are clear deficiencies that needs to be addressed.


Sources cited:

1.Rogers, K. D., & Skabar, A. A. (2014). A Micromanagement Task Allocation System for Real-Time Strategy Games. IEEE Transactions on Computational Intelligence and AI in Games,6(1), 67-77. doi:10.1109/tciaig.2013.2297334
2. Kun Shao, K., Shu, Y., & Zhao, D. (april 2018). StarCraft Micromanagement with Reinforcement Learning and Curriculum Transfer Learning. Neural Networks (IJCNN).