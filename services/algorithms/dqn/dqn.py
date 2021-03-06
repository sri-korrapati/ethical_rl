import sys
from collections import deque
import numpy as np
import tensorflow as tf
from tensorflow import keras
from services.algorithms.dqn import DQNBASE
from services.constants import *

class  Algorithm(DQNBASE):
    def __init__(self, **kwargs):
      super().__init__(**kwargs)

    def _get_target_q_values(self, next_Q_values, rewards, dones, *args):
      max_next_Q_values = np.max(next_Q_values, axis=1)
      target_Q_values = (rewards +
                          (1 - dones) * self.discount_factor * max_next_Q_values)
      target_Q_values = target_Q_values.reshape(-1, 1)
      return target_Q_values


    def train(self):
        rewards = []
        for episode in range(self.number_of_episodes):
            state = self.env.reset()
            total_episode_rewards = 0
            epsilon = self.epsilon_schedule.value(episode) #max(1 - episode / self.number_of_episodes, 0.01) # this can be configurable
            for step in range(self.maximum_step_size):
                state, reward, done, info = self.play_one_step(state, epsilon)
                total_episode_rewards += reward
                if done:
                    break

            if episode >= self.buffer_wait_steps:  # no need to train until the buffer has data
              self._training_step(episode)

            # print(f"episode: {episode} / total_rewards: {total_episode_rewards} / total_steps: {step} / metadata: {self.env.metadata}")
            rewards.append(total_episode_rewards)
        return rewards