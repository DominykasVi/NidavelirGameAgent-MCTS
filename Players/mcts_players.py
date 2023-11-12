from typing import Dict, List
import itertools
from bank import Bank
from card import Card
from coin import Coin
from mcts_simulation import MCTS
from player import Player

class MCTSPlayer(Player):
    def __init__(self, name: str, crystal: int, bank_reference: Bank) -> None:
        super().__init__(name, crystal, bank_reference)
        self.MCT = MCTS()

    def make_bet(self, possible_choices:Dict[int, List[Card]]) -> None:
        possible_bets = list(itertools.permutations(self.coins, 3))
        chosen_bets = MCTS.run_simulation(possible_bets)
            # pass choices to mcts -> one choice
            # super
        
        super().make_bet(chosen_bets)
