from briscola_gym.player.base_player import BasePlayer
from random import randint, random
from briscola_gym.game_rules import select_winner


class EpsGreedyPlayer(BasePlayer):
    def __init__(self, epsilon):
        super().__init__()
        self.epsilon = epsilon
        self.name = 'EpsGreedyPlayer'

    def choose_card(self, table, briscola, state) -> int:
        """
        Choose a card based on epsilon-greedy strategy.
        """
        # Epsilon condition: explore with random action
        if random() < self.epsilon:
            return randint(0, len(self.hand) - 1) if self.hand else 0
        # Otherwise, act greedily
        return self.greedy_action(table, briscola)

    def greedy_action(self, table, briscola) -> int:
        """
        Choose the best card based on the game state.
        """
        im_first = len(table) == 0
        if im_first:
            return self.card_min_points(briscola)  # Minimize points when playing first
        else:
            return self.card_max_gain(table, briscola)  # Maximize gain when responding

    def card_max_gain(self, table, briscola) -> int:
        """
        Choose the card that maximizes gain based on potential outcomes.
        """
        i_max = -1
        max_gain = float('-inf')

        for i, card in enumerate(self.hand):
            table.append(card)
            winner = select_winner(table, briscola)
            coef_pts = 1 if winner == 1 else -1
            gain = coef_pts * sum(c.points for c in table if c)
            if gain > max_gain:
                i_max = i
                max_gain = gain
            table.pop()
        return i_max

    def card_min_points(self, briscola) -> int:
        """
        Choose the card with the minimum points to minimize losses.
        """
        i_min = -1
        min_pts = float('inf')
        for i, card in enumerate(self.hand):
            if card.points == 0 and card.seed != briscola.seed:
                return i
            if card.points < min_pts:
                i_min = i
                min_pts = card.points
        return i_min
