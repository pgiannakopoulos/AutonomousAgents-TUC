import numpy as np
import gym
import _pickle as cPickle

from keras.models import Sequential
from keras.layers import Flatten, Dense, Activation, Embedding, Reshape
from keras.optimizers import Adam

from rl.agents import SARSAAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory
import tensorflow as tf
import os.path
from os import path

tf.compat.v1.disable_eager_execution()

#  pip3 install tensorflow==2.0.0-beta

import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

ENV_NAME = 'Taxi-v3'

# Get the environment and extract the number of actions available in the Cartpole problem
env = gym.make(ENV_NAME)
# env.reset()
np.random.seed(145)
env.seed(145)
nb_actions = env.action_space.n

# model = Sequential()
# model.add(Embedding(500,10,input_length=1))
# model.add(Reshape((10,)))
# model.add(Dense(40, activation='relu'))
# model.add(Dense(40, activation='relu'))
# model.add(Dense(40, activation='relu'))
# model.add(Dense(nb_actions, activation='linear'))
# print(model.summary())

# Next, we build a very simple model.
model = Sequential()
model.add(Dense(500,input_length=1,activation='relu'))
# model.add(Reshape((10,)))
# model.add(Dense(50, activation='relu'))
# model.add(Dense(50, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(nb_actions, activation='linear'))
print(model.summary())

policy = EpsGreedyQPolicy()
deep_sarsa = SARSAAgent(model=model, nb_actions=nb_actions, nb_steps_warmup=500, policy=policy)
deep_sarsa.compile(loss='mse', optimizer=Adam(lr=1e-3), metrics=['mae'])

if(not path.exists('dsarsa_{}_weights.h5f'.format(ENV_NAME))):
	deep_sarsa.fit(env, nb_steps=230000, visualize=False, verbose=1)
	# After training is done, we save the final weights.
	deep_sarsa.save_weights('dsarsa_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
else:
	deep_sarsa.load_weights('dsarsa_{}_weights.h5f'.format(ENV_NAME))
deep_sarsa.test(env, nb_episodes=50000, visualize=False, nb_max_episode_steps=99)