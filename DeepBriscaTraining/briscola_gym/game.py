import logging
from random import randint

from gymnasium.spaces import Box

from briscola_gym.player.base_player import BasePlayer
from gymnasium import spaces, Env
import numpy as np

from briscola_gym.player.epsgreedy_player import EpsGreedyPlayer
from briscola_gym.player.model_player import ModelPlayer

from briscola_gym.game_rules import select_winner
from briscola_gym.card import *
from briscola_gym.player.random_player import PseudoRandomPlayer
from briscola_gym.player.human_player import HumanPlayer


class BriscolaCustomEnemyPlayer(Env):
    def __init__(self, other_player: BasePlayer):
        super().__init__()
        self.action_space = spaces.Discrete(3)  # Drop i-th card
        self.my_player: BasePlayer = HumanPlayer()
        self.other_player = other_player
        self.reward_range = (-44, 44)

        # Core state limits
        core_state_low = np.array([0, 0, 0, 0], dtype=np.float32)
        core_state_high = np.array([120, 120, 40, 1], dtype=np.float32)

        # Card representation limits
        card_low = np.array([0, 0], dtype=np.float32)
        card_high = np.array([10, 4], dtype=np.float32)

        # Binary vector for discarded cards (40 cards, values are 0 or 1)
        discarded_low = np.zeros(40, dtype=np.float32)
        discarded_high = np.ones(40, dtype=np.float32)

        # Max cards in hand and on the table
        max_cards = 5

        # Combine all components
        low = np.concatenate([core_state_low, np.tile(card_low, max_cards), discarded_low])
        high = np.concatenate([core_state_high, np.tile(card_high, max_cards), discarded_high])

        # Define the observation space
        self.observation_space = Box(low=low, high=high, dtype=np.float32)

        self.deck = None
        self.briscola: Card = None
        self.__logger = logging.getLogger('Briscola')
        self.turn_my_player = 0

    def step(self, action):
        if not self.action_space.contains(action):
            raise ValueError(f"Invalid action {action} for action space {self.action_space}")

        self.turn += 1
        if len(self.my_player.hand) < action + 1:
            my_card = self.my_player.hand.pop(len(self.my_player.hand)-1)
        else:
            my_card = self.my_player.hand.pop(action)
        self.table.append(my_card)

        if self.turn_my_player == 0:
            other_card = self.other_player.discard_card(self.table, self.briscola, self.model_state())
            self.table.append(other_card)

        self.__logger.info(f'Table: {self.table}')
        i_winner = select_winner(self.table, self.briscola)
        reward = self._state_update_after_winner(i_winner)
        self._draw_phase()

        if self.turn_my_player == 1 and not self.is_finish():
            other_card = self.other_player.discard_card(self.table, self.briscola, self.model_state())
            self.table.append(other_card)

        done = self.is_finish()
        return self.public_state(), reward, done, False, {}

    def _state_update_after_winner(self, i_winner):
        self.__logger.info(f'Turn Winner is {self.players[i_winner].name}')
        gained_points = sum(values_points[c.value] for c in self.table)

        my_proximity = max(0, self.my_points / 60)
        other_proximity = max(0, self.other_points / 60)

        self.discarded_cards.append(self.table[0])
        self.discarded_cards.append(self.table[1])

        if i_winner == self.turn_my_player:
            importance_factor = 1 + (my_proximity ** 2)  # Reward grows quadratically
            reward = gained_points * importance_factor
            self.my_points += gained_points
            self.turn_my_player = 0
        else:
            importance_factor = 1 + (other_proximity ** 2)
            reward = -gained_points * importance_factor
            self.other_points += gained_points
            self.turn_my_player = 1

        self.my_player.notify_turn_winner(reward)
        self.other_player.notify_turn_winner(-reward)

        self.table = []
        self.__logger.info(f'Winner gained {gained_points} points')
        self.__logger.info(f'Current points: {self.my_points}, {self.other_points}')
        return reward

    def _draw_phase(self):
        if not self.deck.is_empty():
            c1 = self.deck.draw()
            c2 = self.deck.draw()

            if self.turn_my_player == 0:
                self.my_player.hand.append(c1)
                self.other_player.hand.append(c2)
            else:
                self.my_player.hand.append(c2)
                self.other_player.hand.append(c1)

    def model_state(self):
        state = [
            self.other_points,
            self.my_points,
            len(self.deck.cards) if self.deck else 0,
            not self.turn_my_player,
        ]

        if self.briscola is None:
            briscola_state = [0, 0]
        else:
            briscola_state = [self.briscola.value, self.briscola.seed]
        state.extend(briscola_state)

        # Define fixed sizes for each card group
        max_hand_size = 3
        max_table_size = 1

        # Helper function to pad and flatten card groups
        def pad_cards(cards, max_size):
            padded = [[0, 0]] * max_size  # Fill with zeros initially
            for i, card in enumerate(cards[:max_size]):  # Cap to max size
                padded[i] = [card.value, card.seed]
            return np.array(padded).flatten()

        # Pad each card group
        state.extend(pad_cards(self.table, max_table_size))
        state.extend(pad_cards(self.other_player.hand, max_hand_size))

        # Map discarded cards to a binary vector
        total_cards = 40  # 10 values * 4 seeds
        discarded_vector = np.zeros(total_cards, dtype=np.float32)

        for card in self.discarded_cards:
            # Adjust the card indexing for values 1-10 and seeds 1-4
            card_index = (card.value - 1) + ((card.seed - 1) * 10)  # Zero-based indexing
            discarded_vector[card_index] = 1

        state.extend(discarded_vector)

        # Convert to numpy array and pad to match observation space
        state = np.array(state, dtype=np.float32)
        return np.pad(state, (0, self.observation_space.shape[0] - state.size), constant_values=0)

    def public_state(self):
        state = [
            self.my_points,
            self.other_points,
            len(self.deck.cards) if self.deck else 0,
            self.turn_my_player,
        ]

        if self.briscola is None:
            briscola_state = [0, 0]
        else:
            briscola_state = [self.briscola.value, self.briscola.seed]
        state.extend(briscola_state)

        # Define fixed sizes for each card group
        max_hand_size = 3
        max_table_size = 1

        # Helper function to pad and flatten card groups
        def pad_cards(cards, max_size):
            padded = [[0, 0]] * max_size  # Fill with zeros initially
            for i, card in enumerate(cards[:max_size]):  # Cap to max size
                padded[i] = [card.value, card.seed]
            return np.array(padded).flatten()

        # Pad each card group
        state.extend(pad_cards(self.table, max_table_size))
        state.extend(pad_cards(self.my_player.hand, max_hand_size))

        # Map discarded cards to a binary vector
        total_cards = 40  # 10 values * 4 seeds
        discarded_vector = np.zeros(total_cards, dtype=np.float32)

        for card in self.discarded_cards:
            # Adjust the card indexing for values 1-10 and seeds 1-4
            card_index = (card.value - 1) + ((card.seed - 1) * 10)  # Zero-based indexing
            discarded_vector[card_index] = 1

        state.extend(discarded_vector)

        # Convert to numpy array and pad to match observation space
        state = np.array(state, dtype=np.float32)
        return np.pad(state, (0, self.observation_space.shape[0] - state.size), constant_values=0)

    def is_finish(self):
        return ((self.my_points > 60) or (self.other_points > 60) or
               (self.deck.is_empty() and all(len(p.hand) == 0 for p in self.players)))
        #return self.deck.is_empty() and all(len(p.hand) == 0 for p in self.players)

    def reset(self, **kwargs):
        self.turn = 0
        self.my_player.reset_player()
        self.other_player.reset_player()
        self.deck = Deck()
        self.discarded_cards = []
        self.table = []
        self.my_points = 0
        self.other_points = 0
        self.turn_my_player = randint(0, 1)
        self.players = [self.my_player, self.other_player]
        self.briscola: Card = self.deck.draw()

        for _ in range(3):
            self.my_player.hand.append(self.deck.draw())
            self.other_player.hand.append(self.deck.draw())

        self.deck.cards.append(self.briscola)

        if self.turn_my_player == 1:
            other_card = self.other_player.discard_card(self.table, self.briscola, self.model_state())
            self.table.append(other_card)

        return self.public_state(), {}

    def render(self, mode="human"):
        pass


class BriscolaRandomPlayer(BriscolaCustomEnemyPlayer):
    def __init__(self):
        super().__init__(PseudoRandomPlayer())


class BriscolaEpsGreedyPlayer(BriscolaCustomEnemyPlayer):
    def __init__(self, eps):
        super().__init__(EpsGreedyPlayer(eps))

class BriscolaModelPlayer(BriscolaCustomEnemyPlayer):
    def __init__(self, model_path, use_full_model):
        super().__init__(ModelPlayer(model_path, use_full_model))
