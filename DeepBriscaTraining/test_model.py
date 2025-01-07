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
model = DQN.load("models3/dqn_briscola_greedy_1_000_000.zip")

# Create the environment with the random player
env = gym.make("BriscolaRandom-v0")


# Function to simulate a game
def evaluate_agent(model, env, num_games=1000):
    wins = 0
    losses = 0
    draws = 0
    game_rewards = 0
    timesteps_per_game = []
    current_game_timesteps = 0
    total_reward = 0

    for game in range(num_games):
        obs, _ = env.reset()  # Reset the environment at the start of each game
        done = False
        while not done:
            # Get action from the model (deterministic)
            action, _ = model.predict(obs, deterministic=True)

            # Take the action and get the new state and reward
            obs, reward, done, _, info = env.step(action)

            current_game_timesteps += 1
            total_reward += reward
            game_rewards += reward

        timesteps_per_game.append(current_game_timesteps)

        print(f"Game: {game} Reward: {game_rewards} Timesteps: {current_game_timesteps}")

        # Check the result of the game
        if obs[0] > obs[1]:
            wins += 1
        elif obs[0] < obs[1]:
            losses += 1
        else:
            draws += 1

        game_rewards = 0
        current_game_timesteps = 0

    average_timesteps = np.mean(timesteps_per_game) if num_games > 0 else 0
    average_reward = total_reward / num_games if num_games > 0 else 0
    win_percentage = (wins / num_games) * 100 if num_games > 0 else 0
    loss_percentage = (losses / num_games) * 100 if num_games > 0 else 0
    draw_percentage = (draws / num_games) * 100 if num_games > 0 else 0

    return average_timesteps, average_reward, win_percentage, loss_percentage, draw_percentage


# Run the evaluation
average_timesteps, average_reward, win_percentage, loss_percentage, draw_percentage = (evaluate_agent
                                                                                       (model, env, num_games=8000))

# Print the results
print(f"Average timesteps per game: {average_timesteps:.2f}")
print(f"Average reward per game: {average_reward:.2f}")
print(f"Win Percentage: {win_percentage:.2f}%")
print(f"Loss Percentage: {loss_percentage:.2f}%")
print(f"Draw Percentage: {draw_percentage:.2f}%")
