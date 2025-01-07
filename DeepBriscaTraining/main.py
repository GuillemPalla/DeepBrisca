import gymnasium as gym
from gymnasium.envs.registration import register
from stable_baselines3 import DQN
import matplotlib.pyplot as plt
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor, load_results
from stable_baselines3.common.results_plotter import load_results, ts2xy
import numpy as np
from stable_baselines3.common import results_plotter

from TrainingMetricsCallback import TrainingMetricsCallback
from gymnasium.wrappers import TimeLimit

# Register custom environments
register(
    id='BriscolaRandom-v0',
    entry_point='briscola_gym.game:BriscolaRandomPlayer',
)

register(
    id='BriscolaEpsGreedy-v0',
    entry_point='briscola_gym.game:BriscolaEpsGreedyPlayer',
)

log_path = "logs/"

# Create the environment
env = gym.make("BriscolaEpsGreedy-v0")

env = Monitor(env, log_path)

# Initialize the DQN model
model = DQN(
    "MlpPolicy",
    env,
    learning_rate=1e-3,
    buffer_size=500000,
    learning_starts=1000,
    batch_size=128,
    gamma=0.99,
    verbose=1,
    exploration_fraction=0.2,
    exploration_final_eps=0.01,
    target_update_interval=500,
)

# Train the model
callback = TrainingMetricsCallback()
timesteps = 1_000_000
model.learn(total_timesteps=timesteps, callback=callback)

# Save the trained model
model.save("models3/dqn_briscola_greedy_1_000_000")
del model

