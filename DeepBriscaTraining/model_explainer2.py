import gymnasium as gym
from gymnasium.envs.registration import register
import numpy as np
import torch
from pytorch_classes.DQN2 import DQN

# Perturbation analysis function for PyTorch model
def perturbation_analysis(policy_net, observation, feature_idx, delta=0.1):
    modified_obs = observation.clone()
    modified_obs[0, feature_idx] += delta

    with torch.no_grad():
        original_q_values = policy_net(observation).squeeze(0)
        modified_q_values = policy_net(modified_obs).squeeze(0)

    return torch.abs(original_q_values - modified_q_values)

# Evaluate the agent and calculate feature importance
def evaluate_agent_with_importance(policy_net, env, num_games=1000, delta=0.1):
    all_feature_importances = []  # To store feature importances for all observations

    for game in range(num_games):
        obs, _ = env.reset()
        obs = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
        done = False

        while not done:
            with torch.no_grad():
                action = policy_net(obs).max(1).indices.item()

            # Perform perturbation analysis on the current observation
            feature_importances = [
                perturbation_analysis(policy_net, obs, i, delta).mean().item()
                for i in range(obs.shape[1])
            ]
            all_feature_importances.append(feature_importances)

            # Take the action and get the new state and reward
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            obs = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)

        print(f"Game: {game + 1}")

    # Aggregate feature importances
    aggregated_importances = np.mean(all_feature_importances, axis=0)

    return aggregated_importances

# Register environments
register(
    id='BriscolaRandom-v0',
    entry_point='briscola_gym.game:BriscolaRandomPlayer',
)

register(
    id='BriscolaEpsGreedy-v0',
    entry_point='briscola_gym.game:BriscolaEpsGreedyPlayer',
    kwargs={'eps': 0.2},
)

# Feature names for the observation vector
feature_names = [
    "my points", "other points", "length deck", "turn my player",
    "briscola value", "briscola seed", "table card value", "table card seed",
    "hand card 1 value", "hand card 1 seed", "hand card 2 value", "hand card 2 seed",
    "hand card 3 value", "hand card 3 seed"
] + [f"discarded card {i}" for i in range(1, 41)]

# Load the trained model
checkpoint_path = "models3/dqn_greedy-150_000-800KMem-1e_4LR-128BS-NNv2.pth"
checkpoint = torch.load(checkpoint_path, map_location="cpu")

# Create the policy network
n_observations = 54  # Adjust based on observation size
n_actions = 3  # Adjust based on action space size
policy_net = DQN(n_observations, n_actions)
policy_net.load_state_dict(checkpoint["model_state_dict"])
policy_net.eval()

# Create the environment
env = gym.make("BriscolaEpsGreedy-v0")

# Run the evaluation with feature importance
feature_importances = evaluate_agent_with_importance(policy_net, env, num_games=1000)

# Print the results with feature names
print("\nFeature Importances:")
for i, importance in enumerate(feature_importances):
    print(f"{feature_names[i]}: {importance:.4f}")
