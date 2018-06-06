#Copyright @ ECS 170 Project team IF STMT 4 LYFE

import hive_command
from keras.models import Model
from keras.layers import BatchNormalization as BN, LeakyReLU as LR, Dense, add, Input, Flatten
from keras.optimizers import Adam
from keras import regularizers
from keras.callbacks import ModelCheckpoint
import numpy as np
import tensorflow as tf

class Command:
    def __init__(self):

        self.learning_rate = hive_command.INITIAL_LEARNING_RATE
        self.mind = self.fertilize()

    def subjugate(self, state):

        strategies = self.mind.predict(state)

        return strategies.argmax()

    def evolve(self, input_state, target_val, target_prob, count):

        print("Training iteration: ", str(count))
        training_input = []
        prob_output = []
        val_output = []
        for i in range(0, hive_command.BATCH_TRAIN_COUNT * hive_command.BATCH_SIZE):
            num = np.random.random_integers(0, len(input_state) - 1)
            training_input.append(input_state[num])
            prob_output.append(target_prob[num])
            val_output.append(target_val[num])

        name = "Iteration_" + str(count) + "_.hdf5"
        checkpoint = self.checkpoint(count, name)

        self.model.fit(np.array(training_input),
                       [np.array(val_output), np.array(prob_output)],
                       batch_size = hive_command.BATCH_SIZE,
                       epochs = hive_command.EPOCHS,
                       callbacks = checkpoint)

    def checkpoint(self, iteration, name):

        if iteration % hive_command.SAVE_INTERVAL == 0:
            file = open("iteration.txt", 'r+')
            current_count = int(file.readline())
            file.close()
            open("iteration.txt", 'w').close()
            file = open("iteration.txt", 'r+')
            file.write(str(current_count + hive_command.SAVE_INTERVAL))
            file.close()
            return [ModelCheckpoint(name,
                                    verbose=1,
                                    save_best_only=False,
                                    mode='auto')]
        else:
            return []

    def residual_layer(self, initial_input):

        output_1 = Dense(
            hive_command.RES_LAYER_NODE_COUNT,
            use_bias=False,
            activation='sigmoid',
            kernel_regularizer=regularizers.l2(hive_command.L2_REG_CONST)
        )(initial_input)

        output_2 = BN(axis=1)(output_1)

        output_3 = LR()(output_2)

        output_4 = Dense(
            hive_command.RES_LAYER_NODE_COUNT,
            use_bias=False,
            activation='sigmoid',
            kernel_regularizer=regularizers.l2(hive_command.L2_REG_CONST)
        )(output_3)

        output_5 = BN(axis=1)(output_4)

        output_6 = add([initial_input, output_5])

        final_output = LR()(output_6)

        return final_output

    def fertilize(self):

        initial_input = Input(hive_command.INPUT_DIM)

        output_1 = Dense(
            128,
            use_bias=False,
            activation='sigmoid',
            kernel_regularizer=regularizers.l2(hive_command.L2_REG_CONST),
        )(initial_input)

        output_2 = Dense(
            hive_command.RES_LAYER_NODE_COUNT,
            use_bias=False,
            activation='sigmoid',
            kernel_regularizer=regularizers.l2(hive_command.L2_REG_CONST),
        )(output_1)


        output_3 = BN(axis=1)(output_2)

        res_input = LR()(output_3)
        res_output = res_input

        for i in range(0, hive_command.RES_LAYER_COUNT):
            res_output = self.residual_layer(res_input)
            res_input = res_output

        policy = Dense(
            11,
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(hive_command.L2_REG_CONST),
            name = 'policy'
        )(res_output)

        model = Model(inputs=[initial_input], outputs=[policy])

        model.compile(loss='mean_squared_error',
                      optimizer = Adam(lr = hive_command.INITIAL_LEARNING_RATE, beta_1 = 0.9, beta_2 = 0.999, epsilon = 10E-8),
        )

        return model

    def autopsis(self):

        print(self.mind.summary())