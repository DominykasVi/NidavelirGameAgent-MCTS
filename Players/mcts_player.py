from copy import deepcopy
import random
from typing import Dict, List
import itertools
from bank import Bank
from card import Card
from coin import Coin
from game_state import GameState
import MCTS.mcts_simulation as mcts_simulation
from Players.player import Player
from multiprocessing import Process, Manager
from MCTS.mcts_simulation import Node
import math
from timeit import default_timer as timer

class MCTSPlayer(Player):
    def __init__(self, index: int, crystal: int, bank_reference: Bank, c_value:float, depth:int, 
                 type:str='MCTS', max_child_nodes:int=None
                 ,pw:bool=False, c:float=2, alpha:float=0.5
                 ,oma:bool=False, eq_param:float = math.e) -> None:
        super().__init__(index, crystal, bank_reference)
        self.player_type = 'MCTS'
        if type == 'MCTS':
            self.MCTS = mcts_simulation.MCTS()
        self.c_value = c_value
        self.depth = depth
        self.coin_to_increase = None
        self.action_to_perform = None
        self.hero_to_take = None
        self.pw = pw
        self.c = c
        self.alpha = alpha
        self.oma = oma
        self.eq_param = eq_param

    def run_simulation(self, game_state):
        try:
            # start = timer()
            res = self.MCTS.run_simulation(game_state=game_state, mcts_player_index=self.index
                                           , pw=self.pw, c=self.c, alpha=self.alpha
                                           , oma=self.oma, eq_param = self.eq_param
                                           ,parallel=False)
            # end = timer()
            # with open(r'Logs\TestResults\times\3.txt', 'a') as f:
            #     f.write(f'{end-start}\n')
            return res
        except Exception as e:
            raise(e)

    def make_bet(self, possible_choices:Dict[int, List[Card]], game_state:GameState, special_case:str=None) -> None:
        self.action_to_perform = 'Bet'
        game_state_copy = game_state.copy_state()
        game_state_copy.game_id = game_state.game_id

        for player in game_state.players:
            if player.index != self.index:
                game_state_copy.players[player.index].bets = game_state_copy.players[player.index].bets[:game_state_copy.slot_index]
                
        chosen_bets = self.run_simulation(game_state_copy)
        new_bet = chosen_bets.meta_information['bet']
        if chosen_bets.meta_information['bet'] != chosen_bets.game_state.players[self.index].bets:
            raise(Exception('Bets differ from selected'))
        super().make_bet(new_bet)
        self.action_to_perform = None

    
    def take_card(self, cards_to_choose: List[Card], game_state:GameState) -> List[Card]:
        self.action_to_perform = 'Take'
        game_state_copy = game_state.copy_state()
        game_state_copy.game_id = game_state.game_id

        for player in game_state_copy.players:
            if player.index != self.index:
                game_state_copy.players[player.index].bets = game_state_copy.players[player.index].bets[:game_state_copy.slot_index]

        distinction = False
        for card in cards_to_choose:
            if card.index not in game_state_copy.card_deck.cards.keys():
                game_state_copy.card_deck.add_card(card)
                distinction = True
        if distinction:
            game_state_copy.distinction_take_cards = cards_to_choose

        best_node = self.run_simulation(game_state_copy)

        card_to_take = best_node.meta_information['card']
        if 'coin_increased' in best_node.meta_information.keys():
            self.coin_to_increase = best_node.meta_information['coin_increased']
            if self.coin_to_increase not in self.coins:
                raise(Exception("Increasing coin not at hand"))
        if 'hero_taken' in best_node.meta_information.keys():
            self.hero_to_take = best_node.meta_information['hero_taken']
        if 'cards_dicarded' in best_node.meta_information.keys():
            self.cards_to_discard = best_node.meta_information['cards_dicarded']

        self.action_to_perform = None
        return super().take_card(cards_to_choose, card_to_take)
       

    def increase_coin(self, value: int, in_bets=None, game_state:GameState=None):
        if game_state is not None:
            self.action_to_perform = 'TakeCoin'
            game_state_copy = game_state.copy_state()
            game_state_copy.game_id = game_state.game_id
            
            best_node = self.run_simulation(game_state_copy)
            if 'coin_increased' not in best_node.meta_information.keys():
                raise(Exception('Wrong state taken'))
            self.coin_to_increase = best_node.meta_information['coin_increased']
            self.action_to_perform = None

        if self.coin_to_increase is None:
            raise(Exception("No Coin set"))
        
        coin_to_increase = self.coin_to_increase

        if coin_to_increase in self.left_over_coins:
            in_bets = False
        elif coin_to_increase in self.bets:
            in_bets = True
        else:
            in_bets = None
        super().increase_coin(value, coin_to_increase, in_bets)
        self.coin_to_increase = None

    def choose_hero(self, hero_cards: List[Card]) -> Card:
        if self.hero_to_take is None:
            raise(Exception('No hero preselection'))
        return super().choose_hero(hero_cards, self.hero_to_take)
    
    def discard_cards(self, discard_card_count:int, available_colors:List[str]) -> None:
        if self.cards_to_discard == None:
            raise(Exception('No preselected cards to discard'))
        if len(self.cards_to_discard) != discard_card_count:
            raise(Exception('Different count of dicarded cards'))
        if len(self.cards_to_discard) == 2:
            if self.cards_to_discard[0].color == self.cards_to_discard[1].color:
                raise(Exception('Discard the same color.'))
            if self.cards_to_discard[0].color not in available_colors or \
                    self.cards_to_discard[1].color not in available_colors:
                raise(Exception('Illegal color card discarded.'))
        else:
            if self.cards_to_discard[0].color not in available_colors:
                raise(Exception('Discard the same color.'))
            
        return super().discard_cards(self.cards_to_discard)