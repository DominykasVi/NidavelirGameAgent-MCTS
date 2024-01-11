from copy import deepcopy
import random
from typing import Dict, List
import itertools
from bank import Bank
from card import Card
from coin import Coin
from game_state import GameState
import mcts_simulation
import mcts_simulation_wl
import mcts_simulation_lm
import mcts_simulation_vs
import mcts_simulation_ed
from Players.player import Player

class MCTSPlayer(Player):
    def __init__(self, index: int, crystal: int, bank_reference: Bank, c_value, depth, type:str='MCTS', max_child_nodes=None, manager=None) -> None:
        super().__init__(index, crystal, bank_reference)
        self.player_type = 'MCTS'
        if type == 'MCTS':
            self.MCTS = mcts_simulation.MCTS()
        elif type == 'MCTSWL':
            self.MCTS = mcts_simulation_wl.MCTS()
        elif type == 'MCTSLM':
            self.MCTS = mcts_simulation_lm.MCTS()
            self.max_child_nodes = max_child_nodes
        elif type == 'MCTSVS':
            self.MCTS = mcts_simulation_vs.MCTS()
        elif type == 'MCTSED':
            self.MCTS = mcts_simulation_ed.MCTS()
            self.manager = manager
        self.c_value = c_value
        self.depth = depth
        self.coin_to_increase = -1
        self.action_to_perform = None

    def make_bet(self, possible_choices:Dict[int, List[Card]], game_state:GameState, special_case:str=None) -> None:
        self.action_to_perform = 'Bet'
        game_state_copy = game_state.copy_state()

        for player in game_state_copy.players:
            if player.index != self.index:
                game_state_copy.players[player.index].bets = game_state_copy.players[player.index].bets[:game_state_copy.slot_index]
        # game_state_copy.players[self.index].left_over_coins = []

        # possible_bets = list(itertools.permutations(self.coins, 3))
        # initial_coins = deepcopy(game_state.players[1].coins)
                
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
        self.action_to_perform = None
        # print('hi')

    
    def take_card(self, cards_to_choose: List[Card], game_state:GameState, special_case:str=None) -> List[Card]:
        #TODO: random copy
        self.action_to_perform = 'Take'
        game_state_copy = game_state.copy_state()

        for player in game_state_copy.players:
            if player.index != self.index:
                game_state_copy.players[player.index].bets = game_state_copy.players[player.index].bets[:game_state_copy.slot_index]

        if special_case is not None:
            special_case = ('distinction_selection', cards_to_choose)
        best_state = self.MCTS.run_simulation(game_state=game_state_copy, mcts_player_index=self.index, special_case=special_case)

        best_card = set(best_state.players[self.index].card_deck.cards) - set(self.card_deck.cards)
        best_card = next(iter(best_card))
        if best_state.increase_meta_variable is not None:
            self.coin_to_increase = best_state.increase_meta_variable
        return super().take_card(cards_to_choose, best_state.players[self.index].card_deck.cards[best_card])
       

    def increase_coin(self, value: int, in_bets=None):
        if self.coin_to_increase == -1:
            raise("No Coin set")
        
        coin_to_be_increased = self.coin_to_increase['coin']
        in_bets = self.coin_to_increase['in_bets']
        super().increase_coin(value, coin_to_be_increased, in_bets)
        self.coin_to_increase = -1