#Copyright @ ECS 170 Project team IF STMT 4 LYFE

RES_LAYER_COUNT = 5 # Number of residual layers
INPUT_DIM = (1, 50) # Input to NN
L2_REG_CONST = 0.0001 # L2 regularization constant
INITIAL_LEARNING_RATE = 0.02 # Learning rate for fitting
RES_LAYER_NODE_COUNT = 128 # Number of nodes per res layer 

BATCH_TRAIN_COUNT = 50 # Number of mimi-batches per epoch
SAVE_INTERVAL = 5 # How many training iterations before saving the model.
BATCH_SIZE = 4 # Size of each mini-batch
EPOCHS = 1 # Number times a single set of data will be trained


#SARSA(Lambda)
alpha = 0.001
lambda_ = 0.9
gamma = 0.8
episodes = 1000
