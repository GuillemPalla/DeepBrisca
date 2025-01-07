from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import matplotlib.pyplot as plt

class TrainingMetricsCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(TrainingMetricsCallback, self).__init__(verbose)
        self.episode_rewards = []
        self.episode_results = []
        self.current_game_reward = 0
        self.total_episodes = 0

    def _on_step(self) -> bool:
        reward = self.locals["rewards"][0]
        done = self.locals["dones"][0]

        self.current_game_reward += reward

        if done:
            self.total_episodes += 1
            if self.current_game_reward > 0:
                self.episode_results.append(1)  # Win
            elif self.current_game_reward < 0:
                self.episode_results.append(-1)  # Loss
            else:
                self.episode_results.append(0)  # Draw

            self.episode_rewards.append(self.current_game_reward)
            self.current_game_reward = 0

        return True

    def _on_training_end(self) -> None:
        episodes = len(self.episode_results)
        if episodes == 0:
            print("No episodes recorded during training.")
            return

        wins = self.episode_results.count(1)
        losses = self.episode_results.count(-1)
        draws = self.episode_results.count(0)

        win_rate = [np.mean([r == 1 for r in self.episode_results[max(0, i - 50):i + 1]]) for i in range(episodes)]
        loss_rate = [np.mean([r == -1 for r in self.episode_results[max(0, i - 50):i + 1]]) for i in range(episodes)]
        draw_rate = [np.mean([r == 0 for r in self.episode_results[max(0, i - 50):i + 1]]) for i in range(episodes)]

        smoothed_rewards = np.convolve(self.episode_rewards, np.ones(50) / 50, mode="valid")

        print(f"Total episodes recorded: {episodes}/{self.total_episodes}")
        print(f"Win rate: {wins / episodes:.2%}, Loss rate: {losses / episodes:.2%}, Draw rate: {draws / episodes:.2%}")

        plt.figure(figsize=(12, 6))

        plt.subplot(2, 1, 1)
        plt.plot(smoothed_rewards, label="Smoothed Rewards")
        plt.xlabel("Episodes")
        plt.ylabel("Total Reward")
        plt.title("Training Rewards")
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(win_rate, label="Win Rate", color="green")
        plt.plot(loss_rate, label="Loss Rate", color="red")
        plt.plot(draw_rate, label="Draw Rate", color="blue")
        plt.xlabel("Episodes")
        plt.ylabel("Rate")
        plt.title("Win/Loss/Draw Rates")
        plt.legend()

        plt.tight_layout()
        plt.show()
