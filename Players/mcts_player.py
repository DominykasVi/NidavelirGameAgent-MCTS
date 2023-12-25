from copy import deepcopy
import random
from typing import Dict, List
import itertools
from bank import Bank
from card import Card
from coin import Coin
from game_state import GameState
from mcts_simulation import MCTS
from Players.player import Player

class MCTSPlayer(Player):
    def __init__(self, index: int, crystal: int, bank_reference: Bank) -> None:
        super().__init__(index, crystal, bank_reference)
        self.player_type = 'MCTS'
        self.MCTS = MCTS()

    def make_bet(self, possible_choices:Dict[int, List[Card]], game_state:GameState, special_case:str=None) -> None:
        game_state_copy = game_state.copy_state()
        # possible_bets = list(itertools.permutations(self.coins, 3))
        initial_coins = deepcopy(game_state.players[1].coins)
        chosen_bets = self.MCTS.run_simulation(game_state=game_state_copy, mcts_player_index=self.index, special_case=special_case)
        #     # pass choices to mcts -> one choice
        #     # super
        # if sorted(initial_coins, key= lambda x: x.value) != sorted(game_state.players[1].coins, key= lambda x: x.value):
        #     print('debug')
        # if sorted(initial_coins, key= lambda x: x.value) != sorted(chosen_bets.players[1].coins, key= lambda x: x.value):
        #     print('debug')
        # print("Object: ",chosen_bets)
        # print("MCTS bets:", chosen_bets.players[self.index].bets)
        new_bet = chosen_bets.players[self.index].bets
        super().make_bet(new_bet)
        # print('hi')

    
    def take_card(self, cards_to_choose: List[Card], game_state:GameState, special_case:str=None) -> List[Card]:
        #TODO: random copy
        game_state_copy = game_state.copy_state()
        if special_case is not None:
            special_case = ('distinction_selection', cards_to_choose)
        best_state = self.MCTS.run_simulation(game_state=game_state_copy, mcts_player_index=self.index, special_case=special_case)

        best_card = set(best_state.players[self.index].card_deck.cards) - set(self.card_deck.cards)
        best_card = next(iter(best_card))
        return super().take_card(cards_to_choose, best_state.players[self.index].card_deck.cards[best_card])

    def increase_coin(self, value: int):
        iterator = True
        while iterator:
            coin_to_increase = random.choice(self.coins)
            if coin_to_increase.exchangeable == False:
                iterator = False
        super().increase_coin(value, coin_to_increase)