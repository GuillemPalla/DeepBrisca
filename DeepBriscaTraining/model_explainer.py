import gymnasium as gym
from gymnasium.envs.registration import register
from stable_baselines3 import DQN
import numpy as np

register(
    id='BriscolaRandom-v0',
    entry_point='briscola_gym.game:BriscolaRandomPlayer',
)

register(
    id='BriscolaEpsGreedy-v0',
    entry_point='briscola_gym.game:BriscolaEpsGreedyPlayer',
)

# Reload the trained model
model = DQN.load("models/dqn_briscola_greedy_5_000_000_v2")

# Create the environment with the random player
env = gym.make("BriscolaEpsGreedy-v0")


# Function for perturbation analysis
def perturbation_analysis(model, observation, feature_idx, delta=0.1):
    modified_obs = observation.copy()
    modified_obs[feature_idx] += delta
    original_q_values = model.predict(observation, deterministic=True)[0]
    modified_q_values = model.predict(modified_obs, deterministic=True)[0]
    return np.abs(original_q_values - modified_q_values)


# Function to evaluate the agent and calculate feature importance
def evaluate_agent_with_importance(model, env, num_games=1000, delta=0.1):
    all_feature_importances = []  # To store feature importances for all observations

    for game in range(num_games):
        obs, _ = env.reset()  # Reset the environment at the start of each game
        done = False
        while not done:
            # Get action from the model (deterministic)
            action, _ = model.predict(obs, deterministic=True)

            # Perform perturbation analysis on the current observation
            feature_importances = [
                perturbation_analysis(model, obs, i, delta) for i in range(len(obs))
            ]
            all_feature_importances.append(feature_importances)

            # Take the action and get the new state and reward
            obs, reward, done, _, info = env.step(action)

        print(f"Game: {game}")

    # Aggregate feature importances
    aggregated_importances = np.mean(all_feature_importances, axis=0)

    return aggregated_importances


# Feature names for the observation vector
feature_names = [
    "my points", "other points", "length deck", "turn", "turn my player",
    "briscola value", "briscola seed", "table card value", "table card seed",
    "hand card 1 value", "hand card 1 seed", "hand card 2 value", "hand card 2 seed",
    "hand card 3 value", "hand card 3 seed"
] + [f"discarded card {i}" for i in range(1, 41)]  # 15-54 are discarded cards

# Run the evaluation with feature importance
feature_importances = evaluate_agent_with_importance(model, env, num_games=1000)

# Print the results with feature names
print("\nFeature Importances:")
for i, importance in enumerate(feature_importances):
    print(f"{feature_names[i]}: {importance:.4f}")
