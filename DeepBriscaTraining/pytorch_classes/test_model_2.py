import gymnasium as gym
from gymnasium.envs.registration import register
import numpy as np
from pytorch_classes.DQN2 import DQN
import torch
from itertools import count

def test_model(env, policy_net, num_episodes=10):
    stats = {"wins": 0, "losses": 0, "draws": 0}

    for i_episode in range(num_episodes):
        state, info = env.reset()
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        episode_reward = 0

        for t in count():
            # Select the best action using the policy network
            with torch.no_grad():
                action = policy_net(state).max(1).indices.view(1, 1).item()

            # Take the action in the environment
            observation, reward, terminated, truncated, _ = env.step(action)
            episode_reward += reward

            # Prepare the next state
            if terminated or truncated:
                # Determine the outcome of the game
                if observation[0] > observation[1]:
                    stats["wins"] += 1
                elif observation[0] < observation[1]:
                    stats["losses"] += 1
                else:
                    stats["draws"] += 1

                print(f"Episode {i_episode + 1}: Total reward = {episode_reward}")
                break
            state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

    # Print overall statistics
    print("\n--- Testing Results ---")
    print(f"Games Played: {num_episodes}")
    print(f"Wins: {stats['wins']} ({stats['wins'] / num_episodes * 100:.2f}%)")
    print(f"Losses: {stats['losses']} ({stats['losses'] / num_episodes * 100:.2f}%)")
    print(f"Draws: {stats['draws']} ({stats['draws'] / num_episodes * 100:.2f}%)")

def test_agents(env1, env2, num_episodes=10):
    stats = {"agent1_wins": 0, "agent2_wins": 0, "draws": 0}

    for i_episode in range(num_episodes):
        state1, info1 = env1.reset()
        state2, info2 = env2.reset()

        episode_reward1 = 0
        episode_reward2 = 0

        for t in count():
            action1 = env1.action_space.sample()  # Random action for Agent 1
            action2 = env2.action_space.sample()  # Random action for Agent 2

            observation1, reward1, terminated1, truncated1, _ = env1.step(action1)
            observation2, reward2, terminated2, truncated2, _ = env2.step(action2)

            episode_reward1 += reward1
            episode_reward2 += reward2

            if terminated1 or truncated1 or terminated2 or truncated2:
                if observation1[0] > observation2[0]:
                    stats["agent1_wins"] += 1
                elif observation1[0] < observation2[0]:
                    stats["agent2_wins"] += 1
                else:
                    stats["draws"] += 1

                print(f"Episode {i_episode + 1}: Agent1 reward = {episode_reward1}, Agent2 reward = {episode_reward2}")
                break

    # Print overall statistics
    print("\n--- Agent vs Agent Testing Results ---")
    print(f"Games Played: {num_episodes}")
    print(f"Agent1 Wins: {stats['agent1_wins']} ({stats['agent1_wins'] / num_episodes * 100:.2f}%)")
    print(f"Agent2 Wins: {stats['agent2_wins']} ({stats['agent2_wins'] / num_episodes * 100:.2f}%)")
    print(f"Draws: {stats['draws']} ({stats['draws'] / num_episodes * 100:.2f}%)")

register(
    id='BriscolaRandom-v0',
    entry_point='briscola_gym.game:BriscolaRandomPlayer',
)

register(
    id='BriscolaEpsGreedy-v0',
    entry_point='briscola_gym.game:BriscolaEpsGreedyPlayer',
    kwargs={'eps': 0.2},
)

TRAIN_MODEL_PATH = "models3/dqn_greedy_model-550_000-800KMem-1e_4LR-128BS-NNv2.pth"
register(
    id='BriscolaModel-v0',
    entry_point='briscola_gym.game:BriscolaModelPlayer',
    kwargs={'model_path': TRAIN_MODEL_PATH,
            'use_full_model': False},
)

# Create the environment with the random player
env = gym.make("BriscolaModel-v0")

# Create environments for Agent vs Agent testing
env1 = gym.make("BriscolaRandom-v0")
env2 = gym.make("BriscolaEpsGreedy-v0")

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

# Get number of actions from gym action space
n_actions = 3
state, info = env.reset()
n_observations = len(state)

# Load the saved model
checkpoint_path = "models3/dqn_greedy_model-600_000-800KMem-1e_4LR-128BS-NNv2.pth"
checkpoint = torch.load(checkpoint_path, map_location=device)

policy_net = DQN(n_observations, n_actions).to(device)
policy_net.load_state_dict(checkpoint["model_state_dict"]) if "model_state_dict" in checkpoint else policy_net.load_state_dict(checkpoint)
policy_net.eval()  # Set the network to evaluation mode

# Check if optimizer state is available in the checkpoint
if "optimizer_state_dict" in checkpoint:
    print("Optimizer state loaded, but not used for testing.")
else:
    print("No optimizer state found in the checkpoint.")

# Run the test with a model
test_model(env, policy_net, num_episodes=10_000)

# Run the test between two agents
#test_agents(env1, env2, num_episodes=10_000)
