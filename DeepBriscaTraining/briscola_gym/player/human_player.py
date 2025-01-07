from briscola_gym.player.base_player import BasePlayer


class HumanPlayer(BasePlayer):

    def choose_card(self, table, briscola, state) -> int:
        return -1

