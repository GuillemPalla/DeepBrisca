import os

import gymnasium as gym
from gymnasium.envs.registration import register
import math
import random
from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from pytorch_classes.DQN2 import DQN
from pytorch_classes.ReplayMemory import ReplayMemory

def save_model(policy_net, optimizer, model_path):
    torch.save({
        'model_state_dict': policy_net.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, model_path)
    print(f"Model saved to {model_path}")


def load_model(policy_net, target_net, optimizer, model_path, resume_training):
    if resume_training and os.path.exists(model_path):
        checkpoint = torch.load(model_path, map_location=device)
        if 'model_state_dict' in checkpoint:
            policy_net.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            print(f"Full model loaded from {model_path}.")
        else:
            policy_net.load_state_dict(checkpoint)
            print(f"Model state_dict loaded from {model_path}.")
        target_net.load_state_dict(policy_net.state_dict())
    else:
        print("No saved model found. Starting training from scratch.")

def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return policy_net(state).max(1).indices.view(1, 1)
    else:
        return torch.tensor([[env.action_space.sample()]], device=device, dtype=torch.long)

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1).values

    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

print(torch.cuda.is_available())

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

# BATCH_SIZE is the number of transitions sampled from the replay buffer
# GAMMA is the discount factor as mentioned in the previous section
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the ``AdamW`` optimizer
BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4
MEMORY_CAPACITY = 800_000

#env_name = "BriscolaRandom-v0"
#env_name = "BriscolaEpsGreedy-v0"
env_name = "BriscolaModel-v0"
greedy_eps = 0.2
TRAIN_MODEL_PATH = "models3/dqn_greedy_model-550_000-800KMem-1e_4LR-128BS-NNv2.pth"

resume_training = True
MODEL_LOAD_PATH = "models3/dqn_greedy_model-550_000-800KMem-1e_4LR-128BS-NNv2.pth"

num_episodes = 50_000
MODEL_SAVE_PATH = f"test.pth"

# Register custom environments
register(
    id='BriscolaRandom-v0',
    entry_point='briscola_gym.game:BriscolaRandomPlayer',  # Correct path to your custom environment
)

register(
    id='BriscolaEpsGreedy-v0',
    entry_point='briscola_gym.game:BriscolaEpsGreedyPlayer',
    kwargs={'eps': greedy_eps},
)

register(
    id='BriscolaModel-v0',
    entry_point='briscola_gym.game:BriscolaModelPlayer',
    kwargs={'model_path': TRAIN_MODEL_PATH,
            'use_full_model': False},
)

env = gym.make(env_name)

# Get number of actions from gym action space
n_actions = 3
# Get the number of state observations
state, info = env.reset()
n_observations = len(state)

policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(MEMORY_CAPACITY)

steps_done = 0
losses = []
episode_durations = []

load_model(policy_net, target_net, optimizer, MODEL_LOAD_PATH, resume_training)

for i_episode in range(num_episodes):
    if i_episode%100 == 0:
     print(f"Episode: {i_episode}")
    state, info = env.reset()
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    for t in count():
        action = select_action(state)
        observation, reward, terminated, truncated, _ = env.step(action.item())
        reward = torch.tensor([reward], device=device)
        done = terminated or truncated

        if terminated:
            next_state = None
        else:
            next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

        memory.push(state, action, next_state, reward)

        state = next_state

        optimize_model()

        target_net_state_dict = target_net.state_dict()
        policy_net_state_dict = policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        target_net.load_state_dict(target_net_state_dict)

        if done:
            break

save_model(policy_net, optimizer, MODEL_SAVE_PATH)

print('Complete')
